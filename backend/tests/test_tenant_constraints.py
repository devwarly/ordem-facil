import os
from uuid import UUID, uuid4

import pytest
from sqlalchemy import MetaData, Uuid, create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column

from app.database.base import tenant_fk_constraint, tenant_unique_constraint


class ConstraintBase(DeclarativeBase):
    metadata = MetaData()


class TenantParent(ConstraintBase):
    __tablename__ = "test_tenant_parents"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)

    __table_args__ = (tenant_unique_constraint("uq_test_tenant_parents_company_id_id"),)


class TenantChild(ConstraintBase):
    __tablename__ = "test_tenant_children"

    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    company_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)
    parent_id: Mapped[UUID] = mapped_column(Uuid, nullable=False)

    __table_args__ = (
        tenant_fk_constraint(
            "fk_test_tenant_children_company_id_parent_id",
            "parent_id",
            "test_tenant_parents",
        ),
    )


def test_composite_fk_uses_company_id_and_related_id():
    constraint = next(iter(TenantChild.__table__.foreign_key_constraints))

    assert [column.name for column in constraint.columns] == ["company_id", "parent_id"]
    assert constraint.referred_table.name == "test_tenant_parents"
    assert {column.name for column in constraint.referred_table.columns} >= {
        "company_id",
        "id",
    }


@pytest.mark.integration
@pytest.mark.skipif(
    os.getenv("RUN_DB_TESTS") != "1",
    reason="requer PostgreSQL: definir RUN_DB_TESTS=1 e DATABASE_TEST_URL",
)
def test_postgres_rejects_link_between_different_companies():
    url = os.getenv("DATABASE_TEST_URL")
    if not url:
        pytest.skip("DATABASE_TEST_URL não configurado")

    engine = create_engine(url, pool_pre_ping=True)
    ConstraintBase.metadata.drop_all(engine)
    ConstraintBase.metadata.create_all(engine)
    try:
        with Session(engine) as db:
            parent_a = TenantParent(company_id=uuid4())
            parent_b = TenantParent(company_id=uuid4())
            db.add_all([parent_a, parent_b])
            db.commit()
            db.refresh(parent_a)
            db.refresh(parent_b)

            db.add(TenantChild(company_id=parent_b.company_id, parent_id=parent_a.id))
            with pytest.raises(IntegrityError):
                db.commit()
            db.rollback()
    finally:
        ConstraintBase.metadata.drop_all(engine)
