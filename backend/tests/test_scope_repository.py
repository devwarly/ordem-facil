from uuid import uuid4

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.errors import AppError
from app.database.base import Base
from app.models import Company, User
from app.repositories.base import (
    get_scoped,
    list_scoped,
    require_same_company,
    scoped_select,
)


@pytest.fixture
def db() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


def make_company(name: str) -> Company:
    return Company(legal_name=name, email=f"{name.lower()}@example.test")


def make_user(company: Company, email: str, role: UserRole = UserRole.ADMIN) -> User:
    return User(
        company=company,
        name=email.split("@")[0],
        email=email,
        password_hash="hash-teste",
        role=role.value,
    )


def test_list_scoped_returns_only_own_company(db: Session):
    company_a = make_company("Oficina Alfa")
    company_b = make_company("Assistencia Beta")
    db.add_all(
        [
            company_a,
            company_b,
            make_user(company_a, "ana@alfa.test"),
            make_user(company_a, "bruno@alfa.test", UserRole.ATTENDANT),
            make_user(company_b, "diana@beta.test"),
        ]
    )
    db.commit()

    users_a = list_scoped(db, User, company_a.id)

    assert {user.email for user in users_a} == {"ana@alfa.test", "bruno@alfa.test"}


def test_get_scoped_hides_record_from_other_company(db: Session):
    company_a = make_company("Oficina Alfa")
    company_b = make_company("Assistencia Beta")
    user_b = make_user(company_b, "diana@beta.test")
    db.add_all([company_a, company_b, user_b])
    db.commit()

    with pytest.raises(AppError) as exc:
        get_scoped(db, User, user_b.id, company_a.id)

    assert exc.value.status_code == 404
    assert exc.value.code == "NOT_FOUND"
    assert exc.value.message == "Registro não encontrado."


def test_get_scoped_with_invalid_identifier_is_not_found(db: Session):
    company = make_company("Oficina Alfa")
    db.add(company)
    db.commit()

    with pytest.raises(AppError) as exc:
        get_scoped(db, User, "id-invalido", company.id)

    assert exc.value.status_code == 404


def test_scoped_select_always_filters_company(db: Session):
    company = make_company("Oficina Alfa")
    db.add(company)
    db.commit()

    compiled = str(scoped_select(User, company.id))

    assert "users.company_id" in compiled


def test_require_same_company_rejects_foreign_record(db: Session):
    company_a = make_company("Oficina Alfa")
    company_b = make_company("Assistencia Beta")
    user_b = make_user(company_b, "diana@beta.test")
    db.add_all([company_a, company_b, user_b])
    db.commit()
    db.refresh(user_b)

    with pytest.raises(AppError) as exc:
        require_same_company(user_b, company_a.id)

    assert exc.value.status_code == 404


def test_email_is_unique_globally_case_insensitive(db: Session):
    from sqlalchemy.exc import IntegrityError

    company_a = make_company("Oficina Alfa")
    company_b = make_company("Assistencia Beta")
    db.add_all(
        [
            company_a,
            company_b,
            make_user(company_a, "ana@alfa.test"),
            make_user(company_b, "  ANA@ALFA.TEST  "),
        ]
    )

    with pytest.raises(IntegrityError):
        db.commit()
