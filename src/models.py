import os
from urllib.parse import urlparse
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class AppConfig(BaseModel):
    """Модель конфигурации приложения."""

    package_name: str = Field(
        ..., min_length=1, description="Имя пакета не может быть пустым"
    )
    repository_url: str
    test_repo_mode: bool
    package_version: Optional[str] = None
    filter_substring: Optional[str] = None

    @field_validator("repository_url")
    @classmethod
    def validate_url(cls, value: str) -> str:
        """Проверяет, что URL корректен или является локальным путем."""
        parsed = urlparse(value)
        if parsed.scheme in ("http", "https"):
            return value

        # Если это не ссылка, проверяем, является ли это путем к файлу
        if os.path.exists(value) or "/" in value or "\\" in value:
            return value

        raise ValueError(
            "URL должен начинаться с http://, https:// "
            "или быть путем к локальному файлу"
        )