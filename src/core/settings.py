from __future__ import annotations

from functools import lru_cache
from typing import Literal
from urllib.parse import quote_plus

from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    App settings loaded from environment variables (and optionally a local
    `.env`).

    This module is intentionally dependency-light so it can be imported by any
    layer (API, infrastructure, CLI) without pulling the rest of the app.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    APP_NAME: str = "appointment-services"
    ENV: Literal["local", "dev", "staging", "prod"] = "local"
    DEBUG: bool = True

    API_HOST: str = "0.0.0.0"
    API_PORT: int = Field(default=8000, ge=1, le=65535)

    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = Field(default=5470, ge=1, le=65535)
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: SecretStr = SecretStr("admin")
    POSTGRES_DB: str = "appointment_db"

    DATABASE_URL: str | None = None

    # JWT Settings
    JWT_SECRET_KEY: SecretStr = SecretStr(
        "09359a47b78e35d45536993118deb864fff983daaca8b429260f08d406310398"
    )
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, ge=1)

    @computed_field
    def ASYNC_DATABASE_URL(self) -> str:
        """
        SQLAlchemy async URL for asyncpg.

        Example:
        postgresql+asyncpg://user:pass@host:port/db
        """
        if self.DATABASE_URL:
            return self.DATABASE_URL
        password = quote_plus(self.POSTGRES_PASSWORD.get_secret_value())
        return (
            "postgresql+asyncpg://"
            f"{self.POSTGRES_USER}:{password}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
