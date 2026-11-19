from typing import Any
from uuid import UUID

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.core.errors import AppError

NOT_FOUND_MESSAGE = "Registro não encontrado."


def as_uuid(value: UUID | str) -> UUID:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (ValueError, AttributeError, TypeError) as exc:
        raise AppError(404, "NOT_FOUND", NOT_FOUND_MESSAGE) from exc


def not_found() -> AppError:
    """Erro genérico: não distingue 'inexistente' de 'de outra empresa'."""
    return AppError(404, "NOT_FOUND", NOT_FOUND_MESSAGE)


def scoped_select(model: Any, company_id: UUID) -> Select:
    return select(model).where(model.company_id == company_id)


def list_scoped(db: Session, model: Any, company_id: UUID) -> list[Any]:
    return list(db.scalars(scoped_select(model, company_id)).all())


def get_scoped(db: Session, model: Any, record_id: UUID | str, company_id: UUID) -> Any:
    """Busca por ID sempre com o filtro da empresa autenticada."""
    identifier = as_uuid(record_id)
    stmt = select(model).where(model.id == identifier, model.company_id == company_id)
    record = db.scalars(stmt).first()
    if record is None:
        raise not_found()
    return record


def require_same_company(record: Any, company_id: UUID) -> None:
    """Valida propriedade antes de alterar ou relacionar um registro."""
    if record is None or getattr(record, "company_id", None) != company_id:
        raise not_found()
