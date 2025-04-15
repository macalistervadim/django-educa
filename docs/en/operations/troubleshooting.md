# Troubleshooting

## Common Issues

### Django does not start
1. Check container logs:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml logs backend
```

2. Check database connection:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py dbshell
```

3. Check migration status:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py showmigrations
```

### Celery does not process tasks
1. Check worker status:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend celery -A config status
```

2. Check RabbitMQ connection:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml logs rabbitmq
```

### Caching issues
1. Check Redis connection:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec redis redis-cli ping
```

2. Clear cache:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py clear_cache
```

### Errors in logs
1. Check logs in Kibana:
- Open `http://localhost:5601`
- Go to "Discover"
- Select the application log index

2. Check metrics in Grafana:
- Open `http://localhost:3000`
- Go to the "Django Performance" dashboard

### File storage issues
1. Check MinIO availability:
```bash
curl http://localhost:9000/minio/health/live
```

2. Check file permissions:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py collectstatic --dry-run
```

## Common Errors and Solutions

### ERR_CONNECTION_REFUSED
1. Check Nginx status:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps nginx
```

2. Check configuration:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec nginx nginx -t
```

### Database connection failed
1. Check PostgreSQL status:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps postgres
```

2. Check environment variables:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend env | grep DATABASE
```

### Redis connection error
1. Check Redis status:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml ps redis
```

2. Check configuration:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec redis redis-cli info
```

## Profiling and Debugging

### Django Debug Toolbar
Django Debug Toolbar is enabled when running the project in development mode.

## Performance Monitoring

### Prometheus Metrics
1. Check metrics availability:
```bash
curl http://localhost:9090/metrics
```

### Grafana Alerts
1. Configure alerts:
- Open `http://localhost:3000/alerting/list`
- Create a new rule
- Set up trigger conditions

## System Reset

### Full Restart
1. Stop all containers:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml down
```

2. Remove volumes:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml down -v
```

3. Recreate and start:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml up -d --build
```

### Database Reset
1. Remove migrations:
```bash
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
```

2. Recreate migrations:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py makemigrations
```

3. Apply migrations:
```bash
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py migrate
```

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 
