from pydantic import BaseModel, Field, field_validator
from typing import Optional

class AppConfig(BaseModel):
    package_name: str = Field(..., min_length=1, description="Имя пакета не может быть пустым")
    repository_url: str
    test_repo_mode: bool
    package_version: Optional[str] = None
    filter_substring: Optional[str] = None

    # Кастомная валидация URL (дополнительная проверка)
    @field_validator('repository_url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not (v.startswith('http') or v.startswith('/') or v.startswith('./')):
            raise ValueError('URL должен начинаться с http://, https:// или быть локальным путем')
        return v