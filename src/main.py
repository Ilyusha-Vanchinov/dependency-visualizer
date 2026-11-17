import argparse
import sys

from config_loader import load_config
from fetcher import get_dependencies
from graph_builder import DependencyGraph
from visualizer import GraphVisualizer


def main():
    """Точка входа в CLI-приложение."""
    parser = argparse.ArgumentParser(
        description="Инструмент визуализации зависимостей (Этап 5)"
    )
    parser.add_argument(
        "config_path", type=str, help="Путь к YAML файлу конфигурации"
    )
    args = parser.parse_args()

    config = load_config(args.config_path)

    print(f"\nАнализ пакета: {config.package_name}")
    print(f"Режим тестирования: {config.test_repo_mode}")

    builder = DependencyGraph(config, get_dependencies)

    try:
        builder.build(config.package_name)
    except Exception as error:
        print(f"\nКРИТИЧЕСКАЯ ОШИБКА: {error}")
        sys.exit(1)

    builder.print_graph()

    # Вывод порядка загрузки (Этап 4)
    load_order = builder.get_load_order()
    print("\n--- Порядок загрузки (от листьев к корню) ---")
    for index, pkg in enumerate(load_order, 1):
        print(f"{index}. {pkg}")
    print("----------------------------------------------")

    # Вывод диаграммы D2 (Этап 5)
    print("\n--- Диаграмма D2 ---")
    d2_code = GraphVisualizer.generate_d2(builder.graph)
    print(d2_code)
    print("--------------------")


if __name__ == "__main__":
    main()