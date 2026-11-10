import argparse
from config_loader import load_config

def main():
    parser = argparse.ArgumentParser(description="Инструмент визуализации зависимостей (Этап 1)")
    parser.add_argument("config_path", type=str, help="Путь к YAML файлу конфигурации")
    args = parser.parse_args()

    # Загрузка конфигурации (с обработкой ошибок внутри)
    config = load_config(args.config_path)

    # Вывод параметров в формате ключ-значение
    print("\n--- Текущая конфигурация ---")
    print(f"package_name: {config.package_name}")
    print(f"repository_url: {config.repository_url}")
    print(f"test_repo_mode: {str(config.test_repo_mode).lower()}")
    print(f"package_version: {config.package_version}")
    print(f"filter_substring: {config.filter_substring}")
    print("----------------------------\n")
    print("Успешно! Конфигурация загружена.")

if __name__ == "__main__":
    main()