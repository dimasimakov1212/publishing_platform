# Используем базовый образ Python
FROM python:3.11

# Устанавливаем рабочую директорию в контейнере
WORKDIR /code

# Копируем зависимости в контейнер
COPY pyproject.toml poetry.lock /code/
COPY README.md /code/



# Устанавливаем зависимости
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем код приложения в контейнер
COPY . .
