import urllib.parse
import requests
import toml
import json
import os


def get_dependencies(package_name: str, version: str, config) -> list:
    """
    Универсальная функция: возвращает список зависимостей.
    Если test_repo_mode == True, читает локальный JSON.
    Иначе, скачивает Cargo.toml (логика из Этапа 2).
    """
    if config.test_repo_mode:
        return _get_deps_from_test_file(package_name, config.repository_url)
    else:
        return _get_deps_from_github(package_name, version, config.repository_url)


def _get_deps_from_test_file(package_name: str, file_path: str) -> list:
    """Чтение графа из локального JSON-файла для тестов"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Тестовый файл не найден: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)

    # Возвращаем список зависимостей для конкретного пакета
    return graph_data.get(package_name, [])


def _get_deps_from_github(package_name: str, version: str, repo_url: str) -> list:
    """Оригинальная логика скачивания из GitHub (Этап 2)"""
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.netloc == "github.com":
        path = parsed.path.strip('/')
        urls = []
        if version:
            urls.append(f"https://raw.githubusercontent.com/{path}/v{version}/Cargo.toml")
            urls.append(f"https://raw.githubusercontent.com/{path}/{version}/Cargo.toml")
        else:
            urls.append(f"https://raw.githubusercontent.com/{path}/main/Cargo.toml")
            urls.append(f"https://raw.githubusercontent.com/{path}/master/Cargo.toml")

        for url in urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = toml.loads(response.text)
                    deps = data.get("dependencies", {})
                    return list(deps.keys())  # Возвращаем только имена пакетов
            except Exception:
                continue
        raise FileNotFoundError(f"Не удалось найти Cargo.toml в репозитории {repo_url}")
    else:
        raise ValueError("Поддерживаются только GitHub репозитории.")