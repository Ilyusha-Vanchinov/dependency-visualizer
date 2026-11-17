class GraphVisualizer:
    """Класс для генерации текстового представления графа на D2."""

    @staticmethod
    def generate_d2(graph_data: dict) -> str:
        """
        Генерирует D2-код на основе словаря зависимостей.

        :param graph_data: Словарь вида {пакет: [зависимости]}
        :return: Строка с описанием графа на языке D2.
        """
        d2_lines = ["# Код диаграммы D2", ""]

        for package, deps in graph_data.items():
            if not deps:
                # Если у пакета нет зависимостей, просто объявляем узел
                d2_lines.append(f'"{package}"')
                continue

            for dep in deps:
                # Создаем направленное ребро от пакета к зависимости
                d2_lines.append(f'"{package}" -> "{dep}"')

        return "\n".join(d2_lines)