import os
from pathlib import Path

from django.urls import reverse_lazy

from backend.config.utils.vault_secrets import SecretsManager

secrets = SecretsManager()

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_bool(key: str, default: bool) -> bool:
    return os.getenv(key, str(default)).lower() in (
        "true",
        "1",
        "t",
        "y",
        "yes",
    )


def load_list(key: str, default: str | list) -> list:
    return os.getenv(
        key,
        ",".join(default) if isinstance(default, list) else default,
    ).split(",")


SECRET_KEY = secrets.get_secret(
    "django",
    "DJANGO_SECRET_KEY",
    "fallback-secret",
)

ALLOWED_HOSTS = secrets.get_secret("django", "DJANGO_ALLOWED_HOSTS", "").split(
    ",",
)


INSTALLED_APPS = [
    "backend.apps.courses.apps.CoursesConfig",
    "backend.apps.accounts.apps.AccountsConfig",
    "backend.apps.homepage.apps.HomepageConfig",
    "backend.apps.students.apps.StudentsConfig",
    "backend.apps.feedback.apps.FeedbackConfig",
    "daphne",
    "channels",
    "backend.apps.chat.apps.ChatConfig",
    "unfold",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "storages",
    "django.contrib.staticfiles",
    "embed_video",
    "redisboard",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "rest_framework",
    "social_django",
    "django_prometheus",
    "django_cleanup.apps.CleanupConfig",
]

MIDDLEWARE = [
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

TEMPLATES_DIRS = BASE_DIR / "src" / "templates"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIRS],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ROOT_URLCONF = "backend.config.urls"
WSGI_APPLICATION = "backend.config.wsgi.application"
ASGI_APPLICATION = "backend.config.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": secrets.get_secret("django", "POSTGRES_DB", "educa"),
        "USER": secrets.get_secret("django", "POSTGRES_USER", "postgres"),
        "PASSWORD": secrets.get_secret(
            "django",
            "POSTGRES_PASSWORD",
            "pass123",
        ),
        "HOST": secrets.get_secret("django", "POSTGRES_HOST", "database"),
        "PORT": secrets.get_secret("django", "POSTGRES_PORT", "5432"),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

AWS_ACCESS_KEY_ID = "minioadmin"
AWS_SECRET_ACCESS_KEY = "minioadmin"
AWS_STORAGE_BUCKET_NAME = "django"
AWS_LOGS_BUCKET_NAME = "logs"
AWS_S3_ENDPOINT_URL = "http://s3:9000"
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_QUERYSTRING_AUTH = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = False
AWS_S3_USE_SSL = False
AWS_S3_SECURE_URLS = False
AWS_S3_FILE_OVERWRITE = False
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
}

AWS_S3_CUSTOM_DOMAIN = "localhost:9000/django"
AWS_S3_URL_PROTOCOL = "http:"

STORAGES = {
    "default": {
        "BACKEND": "backend.config.storage.MediaStorage",
    },
    "staticfiles": {
        "BACKEND": "backend.config.storage.StaticStorage",
    },
}

STATICFILES_DIRS = [BASE_DIR / "src" / "static"]

STATIC_URL = f"http://localhost:9000/{AWS_STORAGE_BUCKET_NAME}/static/"
MEDIA_URL = f"http://localhost:9000/{AWS_STORAGE_BUCKET_NAME}/media/"

MEDIA_ROOT = None


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_REDIRECT_URL = reverse_lazy("students:student_course_list")

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://redis:6379/0",
    },
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Educa API",
    "DESCRIPTION": "Documentation Educa API",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
        },
    },
}

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "social_core.backends.google.GoogleOAuth2",
    "social_core.backends.github.GithubOAuth2",
)

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = secrets.get_secret(
    "django",
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY",
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = secrets.get_secret(
    "django",
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET",
)

SOCIAL_AUTH_GITHUB_KEY = secrets.get_secret("django", "SOCIAL_AUTH_GITHUB_KEY")
SOCIAL_AUTH_GITHUB_SECRET = secrets.get_secret(
    "django",
    "SOCIAL_AUTH_GITHUB_SECRET",
)

SOCIAL_AUTH_USER_MODEL = "auth.User"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} "
            "{module} {message} {filename}:{lineno}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
        "debug": {
            "format": "{levelname} {asctime} "
            "{module} {message} {filename}:{lineno}",
            "style": "{",
        },
        "json": {
            "format": (
                '{"timestamp": "%(asctime)s", '
                '"level": "%(levelname)s", '
                '"module": "%(module)s", '
                '"message": "%(message)s", '
                '"file": "%(pathname)s", '
                '"line": %(lineno)d}'
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "debug_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "debug",
        },
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                BASE_DIR,
                "logs",
                "backend",
                "errors.log",
            ),
            "formatter": "verbose",
        },
        "rotating_file": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                BASE_DIR,
                "logs",
                "backend",
                "django.log",
            ),
            "maxBytes": 1024 * 1024 * 5,  # 5MB
            "backupCount": 5,
            "formatter": "verbose",
        },
        "elastic": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": os.path.join(
                BASE_DIR,
                "logs",
                "backend",
                "django.log",
            ),
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["elastic"],
            "level": "INFO",  # Продакшн: INFO
            "propagate": True,
        },
        "django.request": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.security": {
            "handlers": ["file"],
            "level": "WARNING",
            "propagate": False,
        },
        "backend.apps.courses": {
            "handlers": ["console", "rotating_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "backend.apps.accounts": {
            "handlers": ["console", "rotating_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "backend.apps.homepage": {
            "handlers": ["console", "rotating_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "backend.apps.students": {
            "handlers": ["console", "rotating_file"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.middleware": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
    },
}
