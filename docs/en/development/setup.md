# Development Environment Setup

## Requirements

### System Requirements
- CPU: 4+ cores
- RAM: 10+ GB
- Disk: 40+ GB
- OS: Linux/macOS/Windows with WSL2

### Software
- Python 3.12+
- Docker Desktop 4.25+
- Docker Compose 2.23+

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/macalistervadim/django-educa.git
cd django-educa
```

### 2. Build and Start the Infrastructure
```bash
# Start core services
docker-compose -f infra/docker/docker-compose-app.yml up --build -d

# Check service status
docker-compose -f infra/docker/docker-compose-app.yml ps

# Start the development server
docker-compose -f infra/docker/docker-compose-dev.yml up --build -d
```

### 3. Initialize Vault
```bash
# Initialize Vault
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault operator init

# Unseal Vault (run 3 times with different keys)
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault operator unseal
```

### 4. Configure Environment Variables
#### Option 1: Using a .env File
```bash
# Create a .env file from the example
cp .env.example .env

# Edit the .env file with your values
nano .env
```

#### Option 2: Using HashiCorp Vault
```bash
# Load secrets via console or UI (links below):
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/django \
  DJANGO_SECRET_KEY='your-secret-key' \
  DJANGO_ALLOWED_HOSTS='localhost,127.0.0.1' \
  DJANGO_SETTINGS_MODULE='backend.config.settings.development'
  
# Create secrets for AWS/MinIO
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/aws \
  AWS_ACCESS_KEY_ID='minioadmin' \
  AWS_SECRET_ACCESS_KEY='minioadmin'
  
# Create secrets for OAuth
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/oauth \
  SOCIAL_AUTH_GOOGLE_OAUTH2_KEY='your-key' \
  SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET='your-secret'
  
# Create secrets for Celery
docker-compose -f infra/docker/docker-compose-app.yml exec vault vault kv put secret/celery \
  CELERY_BROKER_URL="url"
  
# And so on (refer to the .env.example file for details)
```

### 5. Configure MinIO
```bash
# Create a bucket
docker-compose -f infra/docker/docker-compose-app.yml exec s3 mc mb minio/django

# Set public access
docker-compose -f infra/docker/docker-compose-app.yml exec s3 mc policy set public minio/django 
```

### 6. Apply Migrations
```bash
# Create and apply migrations
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py migrate
```

### 7. Load Fixtures
```bash
# Load courses
docker-compose -f infra/docker/docker-compose-dev.yml exec backend python manage.py loaddata backend/apps/courses/fixtures/courses.json
```

### 8. Collect Static Files
```bash
# Collect and upload static files to MinIO
docker-compose -f infra/docker/docker-compose-dev.yml exec backend collectstatic --noinput
```

### 9. Create a Superuser
```bash
# Follow the prompts in the console
docker-compose -f infra/docker/docker-compose-dev.yml exec backend createsuperuser
```

## Installation Verification
After completing all the steps above, wait about 5-10 minutes for all services to fully initialize and check their functionality.  
If you notice instability, refer to the [troubleshooting guide](../operations/troubleshooting.md) and try repeating the steps above.

#### Service Access:
- Backend: http://localhost:8000
- Admin Panel: http://localhost:8000/admin (use the credentials you set during superuser creation)
- API Docs: http://localhost:8000/api/schema/redoc/
- Swagger UI: http://localhost:8000/api/schema/swagger-ui/
- Kibana: http://localhost:5601/
- S3: http://localhost:9001/
- Vault: http://localhost:8200/
- Grafana: http://localhost:3000/
- Flower: http://localhost:5556/

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 
