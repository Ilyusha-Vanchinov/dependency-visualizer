import yaml
import sys
from pydantic import ValidationError
from models import AppConfig

def load_config(file_path: str) -> AppConfig:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            raw_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"ОШИБКА: Файл конфигурации '{file_path}' не найден.")
        sys.exit(1)
    except PermissionError:
        print(f"ОШИБКА: Нет прав на чтение файла '{file_path}'.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"ОШИБКА: Некорректный синтаксис YAML файла.\nДетали: {e}")
        sys.exit(1)

    if not isinstance(raw_data, dict):
        print("ОШИБКА: Корневой элемент YAML должен быть словарем (ключ: значение).")
        sys.exit(1)

    try:
        # Валидация данных через Pydantic
        config = AppConfig(**raw_data)
        return config
    except ValidationError as e:
        print("ОШИБКА: Некорректные значения параметров в конфигурации:")
        for error in e.errors():
            field = error['loc'][0]
            msg = error['msg']
            print(f"  - Параметр '{field}': {msg}")
        sys.exit(1)