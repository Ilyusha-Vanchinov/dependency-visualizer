import argparse
import sys
from config_loader import load_config
from fetcher import fetch_dependencies


def main():
    parser = argparse.ArgumentParser(description="Инструмент визуализации зависимостей (Этап 2)")
    parser.add_argument("config_path", type=str, help="Путь к YAML файлу конфигурации")
    args = parser.parse_args()

    # Загрузка конфигурации
    config = load_config(args.config_path)

    print("\n--- Текущая конфигурация ---")
    print(f"package_name: {config.package_name}")
    print(f"repository_url: {config.repository_url}")
    print(f"package_version: {config.package_version}")
    print("----------------------------\n")

    print(f"Сбор данных о зависимостях для пакета '{config.package_name}' (версия: {config.package_version})...")

    try:
        dependencies = fetch_dependencies(config.repository_url, config.package_version)
    except (ValueError, FileNotFoundError) as e:
        print(f"\nОШИБКА СБОРА ДАННЫХ:\n{e}")
        sys.exit(1)

    print(f"\n--- Прямые зависимости ({len(dependencies)} шт.) ---")
    if not dependencies:
        print("Прямых зависимостей не найдено.")
    else:
        for dep_name, dep_version in dependencies.items():
            # Значение может быть строкой (версией) или словарем (path, git и т.д.)
            if isinstance(dep_version, dict):
                print(f"- {dep_name}: {dep_version}")
            else:
                print(f"- {dep_name}: {dep_version}")
    print("-----------------------------------------\n")
    print("Этап 2 успешно завершен.")


if __name__ == "__main__":
    main()