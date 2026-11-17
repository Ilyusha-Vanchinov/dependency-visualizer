class DependencyGraph:
    """Строит граф зависимостей и вычисляет порядок загрузки."""

    def __init__(self, config, fetch_func):
        self.config = config
        self.fetch_func = fetch_func
        self.graph = {}
        self.visited = set()
        self.recursion_stack = []
        self.post_order = []

    def build(self, root_package: str):
        """Запускает построение графа от корневого пакета."""
        self._dfs(root_package)
        return self.graph

    def _dfs(self, package: str):
        """Рекурсивный обход в глубину."""
        if self.config.filter_substring and \
                self.config.filter_substring in package:
            print(f"  [Фильтр] '{package}' исключен.")
            return

        self.visited.add(package)
        self.recursion_stack.append(package)

        if package not in self.graph:
            self.graph[package] = []

        try:
            dependencies = self.fetch_func(
                package, self.config.package_version, self.config
            )
        except Exception as error:
            print(f"  [!] Ошибка получения данных '{package}': {error}")
            dependencies = []

        for dep in dependencies:
            if self.config.filter_substring and \
                    self.config.filter_substring in dep:
                continue

            if dep not in self.graph[package]:
                self.graph[package].append(dep)

            # Обработка цикла
            if dep in self.recursion_stack:
                cycle_start = self.recursion_stack.index(dep)
                cycle_path = " -> ".join(
                    self.recursion_stack[cycle_start:] + [dep]
                )
                print(f"  [!] Обнаружен цикл: {cycle_path}")
                continue

            if dep not in self.visited:
                self._dfs(dep)

        self.recursion_stack.pop()
        self.post_order.append(package)

    def get_load_order(self) -> list:
        """Возвращает порядок загрузки (реверс пост-ордера)."""
        return self.post_order[::-1]

    def print_graph(self):
        """Выводит граф в консоль."""
        print("\n--- Граф зависимостей ---")
        for pkg, deps in self.graph.items():
            deps_str = ", ".join(deps) if deps else "(нет зависимостей)"
            print(f"{pkg} -> {deps_str}")
        print("-------------------------")