# Указываем базовый образ, на основе которого будет создан наш контейнер.
# В данном случае это официальный образ Python 3.12.3 на основе Alpine Linux,
# который является легковесным дистрибутивом, минимизирующим размер контейнера.
FROM python:3.12.3-alpine

# Устанавливаем рабочую директорию внутри контейнера. Все дальнейшие команды будут выполняться внутри этой директории.
WORKDIR /app

# Устанавливаем Poetry, инструмент для управления зависимостями и виртуальными окружениями в Python.
# Опция --no-cache-dir предотвращает сохранение временных файлов, что уменьшает размер образа.
RUN pip install poetry --no-cache-dir

# Копируем файлы pyproject.toml и poetry.lock из текущей директории на хосте в рабочую директорию контейнера.
# Эти файлы содержат информацию о зависимостях и настройках проекта.
COPY pyproject.toml poetry.lock ./

# Настраиваем Poetry:
# 1. Отключаем создание виртуальных окружений (virtualenvs.create false), чтобы все зависимости устанавливались глобально в контейнере.
# 2. Устанавливаем зависимости проекта с помощью poetry install:
#    - --no-dev: устанавливаем только production-зависимости, без зависимостей для разработки.
#    - --no-interaction: отключаем все интерактивные запросы во время установки.
#    - --no-ansi: отключаем цветной вывод в терминале.
#    - --no-cache: предотвращает использование кэша, что также снижает размер образа.
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi --no-cache;

# Копируем весь остальной исходный код проекта из текущей директории на хосте в рабочую директорию контейнера.
# Это включает в себя все файлы и папки, необходимые для работы приложения.
COPY . .
