import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_cors_origins_parsing():
    settings = Settings(_env_file=None, CORS_ORIGINS="http://a.test, http://b.test ,")

    assert settings.cors_origins == ["http://a.test", "http://b.test"]


def test_production_guardrails():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, APP_ENV="production", APP_DEBUG=True, SECRET_KEY="x" * 40)

    with pytest.raises(ValidationError):
        Settings(
            _env_file=None,
            APP_ENV="production",
            APP_DEBUG=False,
            CORS_ORIGINS="*",
            SECRET_KEY="x" * 40,
        )

    with pytest.raises(ValidationError):
        Settings(_env_file=None, APP_ENV="production", APP_DEBUG=False, SECRET_KEY="curta")


def test_positive_numbers():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, ACCESS_TOKEN_EXPIRE_MINUTES=0)
