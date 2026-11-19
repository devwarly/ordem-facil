import uuid
from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    ForeignKeyConstraint,
    MetaData,
    UniqueConstraint,
    Uuid,
    func,
)
from sqlalchemy.orm import Mapped, declarative_base, mapped_column

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

Base = declarative_base(metadata=MetaData(naming_convention=NAMING_CONVENTION))


class UUIDPrimaryKeyMixin:
    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class CompanyScopedMixin:
    """Coluna obrigatória de contexto para entidades pertencentes a uma empresa."""

    company_id: Mapped[uuid.UUID] = mapped_column(
        Uuid,
        ForeignKey("companies.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )


def tenant_fk_constraint(
    name: str, local_column: str, target_table: str, target_column: str = "id"
) -> ForeignKeyConstraint:
    """FK composta que impede vincular registros de empresas diferentes.

    A tabela alvo precisa declarar `tenant_unique_constraint(...)` com o mesmo
    par `(company_id, id)`, exigido pelo PostgreSQL para a FK composta.
    """
    return ForeignKeyConstraint(
        ["company_id", local_column],
        [f"{target_table}.company_id", f"{target_table}.{target_column}"],
        ondelete="RESTRICT",
        name=name,
    )


def tenant_unique_constraint(name: str) -> UniqueConstraint:
    """Unicidade exigida como alvo de uma FK composta por empresa."""
    return UniqueConstraint("company_id", "id", name=name)


def non_empty_check(column: str) -> CheckConstraint:
    return CheckConstraint(f"length(trim({column})) > 0", name=f"{column}_non_empty")
