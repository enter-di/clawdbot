"""Application configuration loaded from environment variables."""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Telegram
    telegram_bot_token: str

    # Anthropic / Claude
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-6"

    # n8n
    n8n_base_url: str = "http://n8n:5678"
    n8n_webhook_secret: str

    # Redis
    redis_url: str = "redis://redis:6379/0"

    # Security
    allowed_user_ids: list[int] = []
    rate_limit_requests: int = 10
    rate_limit_window_seconds: int = 60

    # Agent behaviour
    max_messages_per_history: int = 20
    max_agent_iterations: int = 5

    # Logging
    log_level: str = "INFO"

    @field_validator("allowed_user_ids", mode="before")
    @classmethod
    def parse_allowed_user_ids(cls, v: object) -> list[int]:
        if isinstance(v, str):
            return [int(uid.strip()) for uid in v.split(",") if uid.strip()]
        return v  # type: ignore[return-value]


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
