"""Baseline inicial: ainda sem tabelas de domínio.

Revision ID: 0001_initial
Revises:
Create Date: 2026-11-18

"""
from typing import Sequence, Union

from alembic import op

revision: str = "0001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """As tabelas de domínio entram nas próximas revisões."""


def downgrade() -> None:
    """Nada a reverter no baseline."""
