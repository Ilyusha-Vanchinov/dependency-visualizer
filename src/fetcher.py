import json
import os
import urllib.parse

import requests
import toml

# Константы (убраны магические числа)
REQUEST_TIMEOUT = 10
GITHUB_DOMAIN = "github.com"


def get_dependencies(package_name: str, version: str, config) -> list:
    """Возвращает список зависимостей для пакета."""
    if config.test_repo_mode:
        return _get_deps_from_test_file(package_name, config.repository_url)
    return _get_deps_from_github(package_name, version, config.repository_url)


def _get_deps_from_test_file(package_name: str, file_path: str) -> list:
    """Читает граф зависимостей из локального JSON-файла."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Тестовый файл не найден: {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        graph_data = json.load(file)

    return graph_data.get(package_name, [])


def _get_deps_from_github(package_name: str, version: str,
                          repo_url: str) -> list:
    """Скачивает и парсит Cargo.toml из репозитория GitHub."""
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.netloc != GITHUB_DOMAIN:
        raise ValueError("Поддерживаются только GitHub репозитории.")

    path = parsed.path.strip("/")
    urls = []

    if version:
        urls.append(
            f"https://raw.githubusercontent.com/{path}/v{version}/Cargo.toml"
        )
        urls.append(
            f"https://raw.githubusercontent.com/{path}/{version}/Cargo.toml"
        )
    else:
        urls.append(
            f"https://raw.githubusercontent.com/{path}/main/Cargo.toml"
        )
        urls.append(
            f"https://raw.githubusercontent.com/{path}/master/Cargo.toml"
        )

    for url in urls:
        try:
            response = requests.get(url, timeout=REQUEST_TIMEOUT)
            if response.status_code == 200:
                data = toml.loads(response.text)
                deps = data.get("dependencies", {})
                return list(deps.keys())
        except requests.RequestException:
            continue

    raise FileNotFoundError(f"Не удалось найти Cargo.toml в {repo_url}")