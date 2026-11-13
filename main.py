import argparse
import sys
from config_loader import load_config
from fetcher import get_dependencies
from graph_builder import DependencyGraph


def main():
    parser = argparse.ArgumentParser(description="Инструмент визуализации зависимостей (Этап 3)")
    parser.add_argument("config_path", type=str, help="Путь к YAML файлу конфигурации")
    args = parser.parse_args()

    config = load_config(args.config_path)

    print("\n--- Текущая конфигурация ---")
    print(f"package_name: {config.package_name}")
    print(f"test_repo_mode: {config.test_repo_mode}")
    print(f"filter_substring: {config.filter_substring}")
    print("----------------------------\n")

    print(f"Построение графа зависимостей для '{config.package_name}'...")

    builder = DependencyGraph(config, get_dependencies)

    try:
        graph = builder.build(config.package_name)
    except Exception as e:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {e}")
        sys.exit(1)

    builder.print_graph()
    print("\nЭтап 3 успешно завершен.")


if __name__ == "__main__":
    main()