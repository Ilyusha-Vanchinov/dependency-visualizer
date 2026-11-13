class DependencyGraph:
    def __init__(self, config, fetch_func):
        self.config = config
        self.fetch_func = fetch_func
        self.graph = {}  # Словарь для хранения графа: {пакет: [зависимости]}
        self.visited = set()  # Уже полностью обработанные пакеты
        self.recursion_stack = []  # Текущий путь для поиска циклов

    def build(self, root_package: str):
        """Запуск обхода графа (DFS)"""
        self._dfs(root_package)
        return self.graph

    def _dfs(self, package: str):
        # 1. Фильтрация: если имя содержит подстроку, пропускаем
        if self.config.filter_substring and self.config.filter_substring in package:
            print(f"  [Фильтр] Пакет '{package}' исключен (содержит '{self.config.filter_substring}')")
            return

        # 2. Помечаем как посещенный и добавляем в текущий путь
        self.visited.add(package)
        self.recursion_stack.append(package)

        if package not in self.graph:
            self.graph[package] = []

        # 3. Получаем зависимости (из теста или GitHub)
        try:
            dependencies = self.fetch_func(package, self.config.package_version, self.config)
        except Exception as e:
            print(f"  [!] Ошибка получения данных для '{package}': {e}")
            dependencies = []

        # 4. Рекурсивный обход зависимостей
        for dep in dependencies:
            # Проверка на фильтр для самой зависимости
            if self.config.filter_substring and self.config.filter_substring in dep:
                continue

            # Добавляем ребро в граф
            if dep not in self.graph[package]:
                self.graph[package].append(dep)

            # Обработка цикла
            if dep in self.recursion_stack:
                cycle_start = self.recursion_stack.index(dep)
                cycle_path = " -> ".join(self.recursion_stack[cycle_start:] + [dep])
                print(f"  [!] Обнаружен цикл: {cycle_path}")
                continue  # Пропускаем рекурсию для этого узла, чтобы не уйти в бесконечность

            # Рекурсивный вызов, если узел еще не посещен
            if dep not in self.visited:
                self._dfs(dep)

        # 5. Завершаем обработку узла (backtracking)
        self.recursion_stack.pop()

    def print_graph(self):
        print("\n--- Граф зависимостей ---")
        for pkg, deps in self.graph.items():
            if deps:
                print(f"{pkg} -> {', '.join(deps)}")
            else:
                print(f"{pkg} -> (нет зависимостей)")
        print("-------------------------")