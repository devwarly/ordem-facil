import os

import pytest
from sqlalchemy import create_engine, text

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(
        os.getenv("RUN_DB_TESTS") != "1",
        reason="requer PostgreSQL: definir RUN_DB_TESTS=1 e DATABASE_TEST_URL",
    ),
]


def test_database_connection_and_migrations():
    url = os.getenv("DATABASE_TEST_URL")
    if not url:
        pytest.skip("DATABASE_TEST_URL não configurado")

    engine = create_engine(url, pool_pre_ping=True)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT 1")).scalar_one() == 1
        tables = {
            row[0]
            for row in connection.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
        }
        assert {"alembic_version", "companies", "users"} <= tables

        indexes = {
            row[0]
            for row in connection.execute(
                text("SELECT indexname FROM pg_indexes WHERE schemaname = 'public'")
            )
        }
        assert "uq_users_email_lower" in indexes
        assert "ix_users_company_id" in indexes

        version = connection.execute(text("SELECT version_num FROM alembic_version")).scalar_one()
        assert version == "0002_company_users"
