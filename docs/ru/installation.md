# 🚀 Запуск проекта Educa в среде разработки

Процесс запуска проекта разделен на два сценария: без Docker и с Docker. Выберите подходящий вариант в зависимости от ваших предпочтений.

## 🚀 Запуск проекта без Docker

### 1. Требования
Перед запуском проекта убедитесь, что у вас установлены следующие инструменты:

- Python 3.12 или выше [Скачать Python](https://www.python.org/downloads/)

### 2. Клонирование репозитория
Клонируйте проект с помощью Git:

```bash
git clone https://github.com/macalistervadim/django-educa
cd django-educa
```

### 3. Установка зависимостей
Для установки зависимостей используйте Poetry:

```bash
pip install poetry
```
Теперь установите все зависимости проекта:

```bash
poetry install
```

### 4. Настройка переменных окружения
Для корректной работы проекта настройте переменные окружения. Для этого:

- Создайте файл .env в корневой директории проекта.
- Скопируйте значения переменных из .env.example в .env.
- Используйте настройки из файла .env для разработки, а .env.prod — для продакшена.

Убедитесь, что файл .env содержит корректные параметры для подключения к базе данных и другие переменные.

### 5. Настройка базы данных
Для локальной разработки настройте подключение к базе данных в файле development.py. Если используется SQLite, настройки будут выглядеть так:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Для использования PostgreSQL настройте подключение, указав правильные параметры в .env.

### 6. Миграции базы данных
После настройки базы данных выполните миграции:

```bash
poetry run python manage.py migrate
```

Это создаст необходимые таблицы в базе данных.

### 7. Компиляция сообщений (i18n)
Скомпилируйте переводы с помощью команды:

```bash
poetry run python manage.py compilemessages
```

### 8. Загрузка фикстур (начальных данных)
Для загрузки фикстур выполните команду:

```bash
poetry run python manage.py loaddata backend/src/fixtures/data.json
```

### 9. Запуск проекта
После выполнения всех шагов запустите сервер:

```bash
poetry run python manage.py runserver
```

Проект должен быть доступен по адресу: http://127.0.0.1:8000/

## 🚀 Запуск проекта с Docker

### 1. Требования
Для запуска проекта с Docker убедитесь, что у вас установлены следующие инструменты:

- Docker [Установить Docker](https://docs.docker.com/get-started/)

### 2. Клонирование репозитория
Клонируйте проект с помощью Git:

```bash
git clone https://github.com/macalistervadim/django-educa
cd django-educa
```

### 3. Настройка переменных окружения
Как и в сценарии без Docker, создайте файл .env и добавьте переменные окружения из .env.example. В зависимости от режима (разработка или продакшен) используйте соответствующие файлы: .env или .env.prod.

### 4. Запуск контейнеров
Для локального запуска используйте файл docker-compose.dev.yml. Это создаст все необходимые контейнеры для разработки (включая базу данных, сервер и другие сервисы):

```bash
docker-compose -f infra/docker/docker-compose.dev.yml up
```

Для продакшен-версии используйте стандартный docker-compose.yml:

```bash
docker-compose -f infra/docker/docker-compose.yml up
```

### 5. Миграции базы данных
Чтобы применить миграции в контейнерах, выполните следующую команду:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py migrate
```

Эта команда выполнит миграции базы данных внутри контейнера, подключаясь к PostgreSQL, если он настроен в вашем .env.

### 6. Компиляция сообщений (i18n)
Скомпилируйте переводы с помощью команды:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py compilemessages
```

### 7. Загрузка фикстур (начальных данных)
Для загрузки фикстур выполните команду:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py loaddata backend/src/fixtures/data.json
```

### 8. Запуск проекта
После выполнения всех настроек и миграций запустите сервер Django:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py runserver
```

Проект будет доступен по адресу http://127.0.0.1:8000/.

## Заметки 📌

Для использования панели администратора Django используйте следующие учетные данные:

```python
логин: admin
пароль: admin
```

Если вы столкнулись с проблемами с зависимостями или настройками, убедитесь, что вы следовали инструкциям в файле .env и правильно настроили все переменные окружения.

Docker и Docker Compose позволяют быстро и легко запустить проект в изолированной среде, избегая конфликтов с локальными зависимостями.

## Дополнительные ресурсы 📚

- [Документация Django](https://docs.djangoproject.com/en/5.1/)
- [Документация DRF](https://www.django-rest-framework.org)
- [Документация Docker](https://docs.docker.com/get-started/)
- [Документация Docker Compose](https://docs.docker.com/compose/)
