# Устранение неполадок

## Общие проблемы

### Django не запускается
1. Проверить логи контейнера:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml logs backend
```

2. Проверить подключение к базе данных:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py dbshell
```

3. Проверить статус миграций:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py showmigrations
```

### Celery не обрабатывает задачи
1. Проверить статус воркеров:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend celery -A config status
```

2. Проверить подключение к RabbitMQ:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml logs rabbitmq
```

### Проблемы с кэшированием
1. Проверить подключение к Redis:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec redis redis-cli ping
```

2. Очистить кэш:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py clear_cache
```

### Ошибки в логах
1. Проверить логи в Kibana:
- Открыть `http://localhost:5601`
- Перейти в "Discover"
- Выбрать индекс с логами приложения

2. Проверить метрики в Grafana:
- Открыть `http://localhost:3000`
- Перейти в дашборд "Django Performance"

### Проблемы с хранением файлов
1. Проверить доступность MinIO:
```bash
curl http://localhost:9000/minio/health/live
```

2. Проверить права доступа:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py collectstatic --dry-run
```

## Частые ошибки и решения

### ERR_CONNECTION_REFUSED
1. Проверить статус Nginx:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps nginx
```

2. Проверить конфигурацию:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec nginx nginx -t
```

### Database connection failed
1. Проверить статус PostgreSQL:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps postgres
```

2. Проверить переменные окружения:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend env | grep DATABASE
```

### Redis connection error
1. Проверить статус Redis:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps redis
```

2. Проверить конфигурацию:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec redis redis-cli info
```

## Профилирование и отладка

### Django Debug Toolbar
В проекте активирован Django Debug Toolbar при запуске проекта
в режиме development

## Мониторинг производительности

### Prometheus метрики
1. Проверка доступности метрик:
```bash
curl http://localhost:9090/metrics
```

### Grafana алерты
1. Настройка оповещений:
- Открыть `http://localhost:3000/alerting/list`
- Создать новое правило
- Настроить условия срабатывания

## Сброс системы

### Полный перезапуск
1. Остановить все контейнеры:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml down
```

2. Удалить волюмы:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml down -v
```

3. Пересоздать и запустить:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml up -d --build
```

### Сброс базы данных
1. Удалить миграции:
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
```

2. Пересоздать миграции:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py makemigrations
```

3. Применить миграции:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py migrate
```
```

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 