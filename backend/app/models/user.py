from sqlalchemy import Boolean, CheckConstraint, Index, String, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.enums import UserRole
from app.database.base import (
    Base,
    CompanyScopedMixin,
    TimestampMixin,
    UUIDPrimaryKeyMixin,
    non_empty_check,
)


class User(CompanyScopedMixin, UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    is_active: Mapped[bool] = mapped_column(
        Boolean, default=True, server_default=text("true"), nullable=False
    )

    __table_args__ = (
        CheckConstraint("role IN ('ADMIN', 'ATTENDANT', 'TECHNICIAN')", name="role"),
        non_empty_check("name"),
        non_empty_check("email"),
        # E-mail de login é único globalmente, ignorando caixa e espaços.
        Index("uq_users_email_lower", func.lower(func.trim(email)), unique=True),
    )

    company: Mapped["Company"] = relationship(  # noqa: F821
        back_populates="users",
        lazy="raise",
    )

    @property
    def role_enum(self) -> UserRole:
        return UserRole(self.role)

    def __repr__(self) -> str:
        return f"<User {self.email!r}>"
