import sys
import yaml
from pydantic import ValidationError

from models import AppConfig


def load_config(file_path: str) -> AppConfig:
    """Загружает и валидирует YAML-файл конфигурации."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            raw_data = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"ОШИБКА: Файл '{file_path}' не найден.")
        sys.exit(1)
    except yaml.YAMLError as error:
        print(f"ОШИБКА: Некорректный синтаксис YAML.\nДетали: {error}")
        sys.exit(1)

    if not isinstance(raw_data, dict):
        print("ОШИБКА: Корневой элемент YAML должен быть словарем.")
        sys.exit(1)

    try:
        return AppConfig(**raw_data)
    except ValidationError as error:
        print("ОШИБКА: Некорректные значения параметров в конфигурации:")
        for err in error.errors():
            field = err["loc"][0]
            print(f"  - Параметр '{field}': {err['msg']}")
        sys.exit(1)