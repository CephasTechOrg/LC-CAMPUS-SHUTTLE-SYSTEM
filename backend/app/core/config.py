from __future__ import annotations

from functools import cached_property
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Campus Shuttle Tracking API"
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/campus_shuttle"
    REDIS_URL: str = "redis://localhost:6379/0"

    JWT_SECRET_KEY: str = "change_this_secret_key_before_production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24

    BACKEND_CORS_ORIGINS: str | list[str] = "*"

    DEFAULT_AVERAGE_SPEED_MPH: float = 20.0
    MIN_VALID_SPEED_MPH: float = 1.0
    MAX_VALID_SPEED_MPH: float = 65.0
    SPEED_SAMPLE_SIZE: int = 10
    STALE_LOCATION_SECONDS: int = 60
    OFFLINE_LOCATION_SECONDS: int = 300
    LIVE_STATE_TTL_SECONDS: int = 900

    FIREBASE_PROJECT_ID: str | None = None
    FIREBASE_CLIENT_EMAIL: str | None = None
    FIREBASE_PRIVATE_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: str | list[str]) -> str | list[str]:
        if isinstance(value, str) and value != "*":
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value

    @cached_property
    def cors_origins(self) -> list[str]:
        value = self.BACKEND_CORS_ORIGINS
        if value == "*":
            return ["*"]
        if isinstance(value, list):
            return value
        return [value]


settings = Settings()
