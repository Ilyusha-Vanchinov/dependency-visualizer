import urllib.parse
import requests
import toml


def get_raw_cargo_url(repo_url: str, version: str) -> list[str]:
    """
    Формирует список возможных URL для скачивания Cargo.toml.
    GitHub использует raw.githubusercontent.com для отдачи сырых файлов.
    """
    parsed = urllib.parse.urlparse(repo_url)
    if parsed.netloc == "github.com":
        path = parsed.path.strip('/')  # получаем owner/repo

        urls = []
        # Теги в Git часто начинаются с 'v' (v1.0.193) или без (1.0.193)
        if version:
            urls.append(f"https://raw.githubusercontent.com/{path}/v{version}/Cargo.toml")
            urls.append(f"https://raw.githubusercontent.com/{path}/{version}/Cargo.toml")
        else:
            # Если версия не указана, пробуем дефолтные ветки
            urls.append(f"https://raw.githubusercontent.com/{path}/main/Cargo.toml")
            urls.append(f"https://raw.githubusercontent.com/{path}/master/Cargo.toml")

        return urls
    else:
        raise ValueError(f"Поддерживаются только GitHub репозитории. Получено: {repo_url}")


def fetch_dependencies(repo_url: str, version: str) -> dict:
    """
    Скачивает Cargo.toml и извлекает прямые зависимости.
    """
    urls = get_raw_cargo_url(repo_url, version)
    content = None
    successful_url = None

    # Пробуем скачать файл по сформированным ссылкам
    for url in urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                content = response.text
                successful_url = url
                break
        except requests.RequestException:
            continue

    if not content:
        raise FileNotFoundError(
            f"Не удалось найти файл Cargo.toml в репозитории.\n"
            f"Проверены URL: {urls}\n"
            f"Убедитесь, что URL и версия (тег) указаны верно."
        )

    # Парсим TOML
    try:
        data = toml.loads(content)
    except toml.TomlDecodeError as e:
        raise ValueError(f"Ошибка синтаксиса в файле Cargo.toml ({successful_url}):\n{e}")

    # Извлекаем прямые зависимости
    # В Cargo.toml они могут быть в [dependencies] или [dev-dependencies] / [build-dependencies]
    # По заданию нужны "прямые зависимости", обычно это [dependencies]
    deps = data.get("dependencies", {})
    return deps