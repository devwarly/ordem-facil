import pytest
from fastapi.testclient import TestClient

from app.database.session import get_db
from app.main import create_app


class FakeSession:
    """Session mínima para testar o endpoint de saúde sem PostgreSQL."""

    def __init__(self) -> None:
        self.executed: list[str] = []

    def execute(self, statement, *args, **kwargs):
        self.executed.append(str(statement))
        return self

    def close(self) -> None:
        pass


@pytest.fixture
def fake_db() -> FakeSession:
    return FakeSession()


@pytest.fixture
def client(fake_db: FakeSession):
    app = create_app()
    app.dependency_overrides[get_db] = lambda: fake_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
