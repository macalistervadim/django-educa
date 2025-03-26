# 🚀 Launching the Suncov Project in Development Environment

The process of launching the project is divided into two scenarios: without Docker and with Docker. Choose the appropriate option based on your preferences.

## 🚀 Launching the Project without Docker

### 1. Requirements
Before starting the project, make sure you have the following tools installed:

- Python 3.12 or higher [Download Python](https://www.python.org/downloads/)

### 2. Clone the Repository
Clone the project using Git:

```bash
git clone https://github.com/macalistervadim/django-educa
cd django-educa
```

### 3. Install Dependencies
To install dependencies, use Poetry:

```bash
pip install poetry
```
Now install all project dependencies:

```bash
poetry install
```

### 4. Configure Environment Variables
To ensure the project works correctly, configure the environment variables. To do this:

- Create a .env file in the root directory of the project.
- Copy the variable values from .env.example to .env.
- Use the settings from the .env file for development, and .env.prod for the production environment.

Make sure the .env file contains the correct parameters for database connection and other variables.

### 5. Configure the Database
For local development, configure the database connection in the development.py file. If using SQLite, the settings will look like this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

To use PostgreSQL, configure the connection by specifying the correct parameters in .env.

### 6. Database Migrations
After configuring the database, run the migrations:

```bash
poetry run python manage.py migrate
```

This will create the necessary tables in the database.

### 7. Compile Messages (i18n)
Compile translations using the command:

```bash
poetry run python manage.py compilemessages
```

### 8. Load Fixtures (Initial Data)
To load fixtures (initial data), run the command:

```bash
poetry run python manage.py loaddata backend/src/fixtures/data.json
```

### 9. Launch the Project
After completing the above steps, start the server:

```bash
poetry run python manage.py runserver
```

The project should now be accessible at: http://127.0.0.1:8000/

## 🚀 Launching the Project with Docker

### 1. Requirements
To launch the project using Docker, make sure you have the following tools installed:

- Docker [Install Docker](https://docs.docker.com/get-started/)

### 2. Clone the Repository
Clone the project using Git:

```bash
git clone https://github.com/macalistervadim/django-educa
cd django-educa
```

### 3. Configure Environment Variables
As with the non-Docker scenario, create a .env file and add the environment variables from .env.example. Depending on the mode (development or production), use the corresponding files: .env or .env.prod.

### 4. Launch Containers
For local launch, use the docker-compose.dev.yml file. This will create all necessary containers for development (including the database, server, and other services):

```bash
docker-compose -f infra/docker/docker-compose.dev.yml up
```

For the production version, use the standard docker-compose.yml:

```bash
docker-compose -f infra/docker/docker-compose.yml up
```

### 5. Database Migrations
To apply migrations in the containers, run the following command:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py migrate
```

This command will run the database migrations inside the container, connecting to PostgreSQL if configured in your .env.

### 6. Compile Messages (i18n)
Compile translations using the command:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py compilemessages
```

### 7. Load Fixtures (Initial Data)
To load fixtures, run the command:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py loaddata backend/src/fixtures/data.json
```

### 8. Launch the Project
After completing all settings and migrations, start the Django server:

```bash
export PYTHONPATH=/app &&
docker-compose exec backend poetry run python manage.py runserver
```

The project will now be accessible at http://127.0.0.1:8000/.

## Notes 📌

To use the Django admin panel, use the following credentials:

```python
login: admin
password: admin
```

If you encounter issues with dependencies or settings, ensure you follow the instructions in the .env file and have correctly configured all environment variables.

Docker and Docker Compose allow you to quickly and easily launch the project in an isolated environment, avoiding conflicts with local dependencies.

## Additional Resources 📚

- [Django Documentation](https://docs.djangoproject.com/en/5.1/)
- [DRF Documentation](https://www.django-rest-framework.org)
- [Docker Documentation](https://docs.docker.com/get-started/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
