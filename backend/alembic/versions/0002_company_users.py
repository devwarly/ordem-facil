"""Cria companies e users com contexto de empresa e e-mail único global.

Revision ID: 0002_company_users
Revises: 0001_initial
Create Date: 2026-11-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "0002_company_users"
down_revision: Union[str, None] = "0001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "companies",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("legal_name", sa.String(length=180), nullable=False),
        sa.Column("trade_name", sa.String(length=180), nullable=True),
        sa.Column("document", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("phone", sa.String(length=30), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("length(trim(legal_name)) > 0", name="legal_name_non_empty"),
        sa.CheckConstraint("length(trim(email)) > 0", name="email_non_empty"),
        sa.UniqueConstraint("document", name="uq_companies_document"),
        sa.PrimaryKeyConstraint("id", name="pk_companies"),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("company_id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=30), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint("role IN ('ADMIN', 'ATTENDANT', 'TECHNICIAN')", name="role"),
        sa.CheckConstraint("length(trim(name)) > 0", name="name_non_empty"),
        sa.CheckConstraint("length(trim(email)) > 0", name="email_non_empty"),
        sa.ForeignKeyConstraint(
            ["company_id"],
            ["companies.id"],
            name="fk_users_company_id_companies",
            ondelete="RESTRICT",
        ),
        sa.PrimaryKeyConstraint("id", name="pk_users"),
    )
    op.create_index("ix_users_company_id", "users", ["company_id"], unique=False)
    op.create_index(
        "uq_users_email_lower",
        "users",
        [sa.text("lower(trim(email))")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("uq_users_email_lower", table_name="users")
    op.drop_index("ix_users_company_id", table_name="users")
    op.drop_table("users")
    op.drop_table("companies")
