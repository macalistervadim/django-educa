# Настройка окружения разработки

## Требования

### Системные требования
- CPU: 4+ ядра
- RAM: 10+ GB
- Disk: 40+ GB
- OS: Linux/macOS/Windows с WSL2

### Программное обеспечение
- Python 3.12+
- Docker Desktop 4.25+
- Docker Compose 2.23+

## Установка

### 1. Клонирование репозитория
```bash
git clone https://github.com/macalistervadim/django-educa.git
cd django-educa
```

### 2. Сборка и запуск инфраструктуры
```bash
# Запуск базовых сервисов
docker-compose -f infra/docker/docker-compose-app.yml up --build -d

# Проверка статуса сервисов
docker-compose -f infra/docker/docker-compose-app.yml ps

# Запуск development сервера
docker-compose -f infra/docker/docker-compose-dev.yml up --build -d
```

### 3. Инициализация Vault
```bash
# Инициализация Vault
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault operator init

# Распечатывание Vault (выполнить 3 раза с разными ключами)
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault operator unseal```
```

### 4. Настройка переменных окружения
#### Вариант 1: Использование .env файла 
```bash
# Создание .env файла из примера
cp .env.example .env

# Отредактируйте .env файл, указав свои значения
nano .env
```

#### Вариант 2: Использование HashiCorp Vault
```bash
# Загрузите секреты через консоль, или через UI интерфейс (ссылки ниже):
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/django \
  DJANGO_SECRET_KEY='your-secret-key' \
  DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1' \
  DJANGO_SETTINGS_MODULE='backend.config.settings.development'
  
# Создание секретов для AWS/MinIO
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/aws \
  AWS_ACCESS_KEY_ID='minioadmin' \
  AWS_SECRET_ACCESS_KEY='minioadmin'
  
# Создание секретов для OAuth
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/oauth \
  SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='your-key' \
  SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='your-secret'
  
# Создание секретов для Celery
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/celery \
  CELERY_BROKER_URL="url"
  
# и так далее (смотрите пример из .env.example)
```

### 5. Настройка MinIO
```bash
# Создание бакета
docker-compose -f infra/docker/docker-compose-app.yml exec s3 mc mb minio/django

# Установка публичного доступа
docker-compose -f infra/docker/docker-compose-app.yml exec s3 mc policy set public minio/django 
```

### 6. Применение миграций
```bash
# Создание и применение миграций
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py migrate
```

### 7. Загрузка фикстур
```bash
# Загрузка курсов
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py loaddata backend/apps/courses/fixtures/courses.json
```

### 8. Сборка статики
```bash
# Сборка и выгрузка в Minio статических файлов
docker-compose -f infra/docker/docker-compose-dev.yml exec backend collectstatic --noinput
```

### 9. Создание суперпользователя
```bash
# Следуйте указаниям в консоли
docker-compose -f infra/docker/docker-compose-dev.yml exec backend createsuperuser
```

## Проверка установки
После выполнения всех шагов выше подождите около 5-10 минут для полной установки всех сервисов и проверьте их работоспособность.
Если заметите нестабильность в работе, используйте инструкцию по устранению [ошибок](../operations/troubleshooting.md) а также попробуйте
выполнить все шаги выше заново 

#### Доступ к сервисам:
- Backend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin (данные, которые вы указывали при создании суперюзера)
- API Docs: http://localhost:8000/api/schema/redoc/
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- Kibana: http://localhost:5601/
- S3: http://localhost:9001/
- Vault: http://localhost:8200/
- Grafana: http://localhost:3000/
- Flower: http://localhost:5556/

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 


