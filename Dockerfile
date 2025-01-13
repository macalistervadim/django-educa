FROM python:3.12

# Устанавливаем зависимости для poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл pyproject.toml и poetry.lock, если они есть, для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости через poetry
RUN poetry install --no-interaction --no-ansi

# Устанавливаем порты и команду
EXPOSE 8000
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
