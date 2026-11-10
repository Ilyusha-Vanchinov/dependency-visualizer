## Проверка работы (Этап 1)

Для проверки работоспособности приложения и демонстрации обработки ошибок выполните следующие шаги.

### 1. Успешный запуск (Вывод параметров)
Убедитесь, что в файле `configs/config.yaml` указаны корректные данные, и запустите программу:
```bash
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
--- Текущая конфигурация ---
package_name: requests
repository_url: https://github.com/psf/requests
test_repo_mode: true
package_version: 2.31.0
filter_substring: req
----------------------------

Успешно! Конфигурация загружена.
```

### 2. Демонстрация обработки ошибок

Приложение перехватывает ошибки и выводит понятные сообщения на русском языке вместо стандартных стектрейсов Python. Для проверки внесите изменения в config.yaml и запустите программу заново.

#### А) Ошибка: Файл не найден (FileNotFound)

Действие: Запустите программу с несуществующим путем: 
```
python main.py configs/wrong_file.yaml
```

Ожидаемый вывод: 
```
ОШИБКА: Файл конфигурации 'configs/wrong_file.yaml' не найден.
```

#### Б) Ошибка: Синтаксис YAML (YAMLError)

Действие: Действие: Откройте config.yaml и удалите закрывающую скобку( "package_name: [requests " ).Запустите программу: 
```
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
ОШИБКА: Некорректный синтаксис YAML файла.
Детали: while parsing a flow sequence
  in "configs/config.yaml", line 1, column 15
expected ',' or ']', but got '<stream end>'
  in "configs/config.yaml", line 1, column 24
```

#### В) Ошибка: Отсутствует обязательный параметр (Pydantic)

Действие: В config.yaml переименуйте package_name в package_nam. Запустите программу: 
```
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
ОШИБКА: Некорректные значения параметров в конфигурации:
  - Параметр 'package_name': Field required
```

#### Г) Ошибка: Неверный тип данных (Pydantic)

Действие: Измените логическое значение на список( "test_repo_mode: [1, 2]" ). Запустите программу: 
```
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
ОШИБКА: Некорректные значения параметров в конфигурации:
  - Параметр 'test_repo_mode': Input should be a valid boolean
```

#### Д) Ошибка: Кастомная валидация URL

Действие: Укажите URL без протокола http:// или https://( "repository_url: "github.com/psf/requests"" ). Запустите программу: 
```
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
ОШИБКА: Некорректные значения параметров в конфигурации:
  - Параметр 'repository_url': Value error, URL должен начинаться с http://, https:// или быть локальным путем
```

## Проверка работы (Этап 2)

### 1. Успешный запуск (Вывод параметров)
```
python main.py configs/config.yaml
```

Ожидаемый вывод:
```
--- Текущая конфигурация ---                                                                                                                                                  
package_name: anyhow                                                                                                                                                          
repository_url: https://github.com/dtolnay/anyhow                                                                                                                             
package_version: 1.0.75                                                                                                                                                       
----------------------------

Сбор данных о зависимостях для пакета 'anyhow' (версия: 1.0.75)...

--- Прямые зависимости (1 шт.) ---
- backtrace: {'version': '0.3.51', 'optional': True}
-----------------------------------------

Этап 2 успешно завершен.
```

### 2. Демонстрация обработки ошибок

Действие: Укажите в конфиге package_version: "999.999.999". Запустите программу: 
```
python main.py configs/config.yaml
```

Ожидаемый вывод: 
```
--- Текущая конфигурация ---                                                                          
package_name: anyhow                                                                                   
repository_url: https://github.com/dtolnay/anyhow   
package_version: 999.999.999                                                               
----------------------------

Сбор данных о зависимостях для пакета 'anyhow' (версия: 999.999.999)...

ОШИБКА СБОРА ДАННЫХ:
Не удалось найти файл Cargo.toml в репозитории.
Проверены URL: ['https://raw.githubusercontent.com/dtolnay/anyhow/v999.999.999/Cargo.toml', 'https://raw.githubusercontent.com/dtolnay/anyhow/999.999.999/Cargo.toml']
Убедитесь, что URL и версия (тег) указаны верно.
```
