from functools import lru_cache
from typing import Literal

from pydantic import field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "OrdemFacil"
    APP_ENV: Literal["development", "test", "production"] = "development"
    APP_DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+psycopg://usuario:senha@localhost:5432/ordemfacil"
    DATABASE_TEST_URL: str | None = None

    SECRET_KEY: str = "substitua-por-uma-chave-aleatoria-por-ambiente"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: str = "http://localhost:5500,http://127.0.0.1:5500"
    SIGNUP_RATE_LIMIT_PER_HOUR: int = 5

    @property
    def cors_origins(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

    @field_validator("ACCESS_TOKEN_EXPIRE_MINUTES", "REFRESH_TOKEN_EXPIRE_DAYS", "SIGNUP_RATE_LIMIT_PER_HOUR")
    @classmethod
    def positive_numbers(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("deve ser maior que zero")
        return value

    @model_validator(mode="after")
    def production_guardrails(self) -> "Settings":
        if self.APP_ENV == "production":
            if self.APP_DEBUG:
                raise ValueError("APP_DEBUG deve ser false em produção")
            if not self.cors_origins or "*" in self.cors_origins:
                raise ValueError("CORS_ORIGINS deve conter origens explícitas em produção")
            if len(self.SECRET_KEY) < 32 or self.SECRET_KEY.startswith("substitua"):
                raise ValueError("SECRET_KEY deve ser forte e exclusiva em produção")
        return self


@lru_cache
def get_settings() -> Settings:
    return Settings()
