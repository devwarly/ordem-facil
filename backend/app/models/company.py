from sqlalchemy import Boolean, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base, TimestampMixin, UUIDPrimaryKeyMixin, non_empty_check


class Company(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "companies"
    __table_args__ = (
        non_empty_check("legal_name"),
        non_empty_check("email"),
        UniqueConstraint("document", name="document"),
    )

    legal_name: Mapped[str] = mapped_column(String(180), nullable=False)
    trade_name: Mapped[str | None] = mapped_column(String(180), nullable=True)
    document: Mapped[str | None] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(30), nullable=True)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False
    )

    users: Mapped[list["User"]] = relationship(  # noqa: F821
        back_populates="company",
        lazy="raise",
    )

    def __repr__(self) -> str:
        return f"<Company {self.legal_name!r}>"


# Importado no fim para evitar import circular entre modelos.
from app.models.user import User  # noqa: E402
