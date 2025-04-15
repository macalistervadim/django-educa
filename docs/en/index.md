# Django Educa - Modern Educational Platform

## Project Overview

Django Educa is a modern educational platform built with Django 5 and Python 3.12. The platform provides a comprehensive solution for online learning with advanced content management capabilities and user interaction features.

## Key Features

### Architectural Solutions
- Monolith with dedicated infrastructure services
- Asynchronous communication via Celery and RabbitMQ
- Multi-level caching using Redis
- Fault-tolerant data storage in PostgreSQL

### Technology Stack
- **Backend**: Django 5, Python 3.12
- **Data Storage**: PostgreSQL, Redis, MinIO (S3-compatible storage)
- **Request Proxying**: Nginx
- **Queues and Workers**: Celery, RabbitMQ
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack (Elasticsearch, Logstash, Kibana)
- **Security**: Vault (secrets management)

### Functionality
- Course Management System (CMS)
- Support for various content types (text, video, files)
- Interactive WebSocket-based chat
- OAuth2 authentication (Google, GitHub)
- REST API with automatic documentation

!!!warning "Minimum Requirements"
    - Docker and Docker Compose
    - 4GB RAM
    - 40GB free disk space
    - Processor with virtualization support

## Quick Start

See the [installation guide](./development/setup.md)

## Architecture
The platform is built on modern architectural patterns:

- Multi-layer architecture: separation into presentation, business logic, and data layers
- Event-driven architecture: asynchronous event processing via Celery
- Monolith with containerized infrastructure: main application is a Django monolith, surrounded by separate services (PostgreSQL, Redis, MinIO, Vault, etc.) deployed in separate Docker containers
- API-first design: fully documented REST API

## License
This project is licensed under the MIT License. See the [LICENCE](../LICENCE.md) file for details.

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div>