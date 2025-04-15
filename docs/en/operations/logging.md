# Logging and Monitoring System

## Overview
Django Educa employs a comprehensive approach to logging and monitoring, including:
- Centralized log collection via the ELK Stack
- Performance metrics through Prometheus and Grafana
- Queue monitoring via Flower
- Nginx logs for traffic analysis

## Technology Stack
- **Elasticsearch**: Log storage and indexing
- **Logstash**: Log processing and transformation
- **Kibana**: Log visualization and analysis
- **Prometheus**: Metrics collection
- **Grafana**: Metrics visualization
- **Flower**: Celery monitoring

## Logging Configuration

### Django Logging
The system uses multi-level logging with JSON formatting for ELK:

- **INFO**: General application information
- **WARNING**: Warnings and non-critical errors
- **ERROR**: Critical errors and exceptions
- **DEBUG**: Debugging information (development only)

### Application Logs
Each application has its own logger:
- `backend.apps.courses`
- `backend.apps.accounts`
- `backend.apps.homepage`
- `backend.apps.students`

### Nginx Logs
Nginx logs are stored in the `/var/log/nginx/` directory:
- `access.log`: HTTP requests
- `error.log`: Server errors

## Monitoring

### Prometheus Metrics
Available at the `/metrics` endpoint:
- HTTP requests
- Response time
- Memory usage
- Database status

### Grafana Dashboards
Key dashboards:
- Django Performance

### Celery Monitoring
Flower is available on port 5556:
- Active tasks
- Execution statistics
- Worker status

## Access

### ELK Stack
- Kibana: `http://localhost:5601`
- Elasticsearch: `http://localhost:9200`

### Metrics
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3000`
- Flower: `http://localhost:5556`

## Log Retention
- Log rotation every 24 hours
- Retention for 30 days
- Automatic compression of old logs

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 