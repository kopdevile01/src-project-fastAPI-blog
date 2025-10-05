from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://fastapi_user:fastapi_password@localhost:5432/fastapi_blog_db"
    )
    test_database_url: str | None = None

    jwt_secret: str = "CHANGE_ME"
    jwt_alg: str = "HS256"
    jwt_exp_minutes: int = 60

    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "noreply@example.com"

    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
