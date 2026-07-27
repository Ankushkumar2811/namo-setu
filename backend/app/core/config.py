from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration loaded exclusively from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_prefix="NAMO_", extra="ignore")

    app_name: str = "NAMO SETU API"
    environment: str = "development"
    api_prefix: str = "/api/v1"
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/namo_setu"
    redis_url: str = "redis://localhost:6379/0"
    jwt_secret: str = Field(default="development-only-change-me", min_length=24)
    jwt_issuer: str = "namo-setu"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    cors_origins: str = "http://localhost:5173,https://namo-setu.vercel.app"
    requests_per_minute: int = 120
    openai_api_key: str | None = None
    openai_model: str = "gpt-5.6"
    ai_provider: str = "openai"
    ai_max_parallel_agents: int = 4
    ai_daily_budget_usd: float = 100.0
    qdrant_url: str | None = None
    qdrant_api_key: str | None = None

    @property
    def allowed_origins(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Return one validated settings instance per process."""
    return Settings()
