import dotenv

from src.config.settings.base import *  # noqa: F403

dotenv.load_dotenv()

DEBUG = False

SECURE_SSL_REDIRECT = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
CORS_ALLOW_CREDENTIALS = True
X_FRAME_OPTIONS = "SAMEORIGIN"
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
CORS_ALLOWED_ORIGINS = load_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    ["https://my-domain.ru"],
)
CSRF_TRUSTED_ORIGINS = load_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    ["https://my-domain.ru"],
)
CORS_ALLOW_HEADERS = [
    "content-type",
    "accept",
    "origin",
    "authorization",
    "x-csrftoken",
    "cross-origin-opener-policy",
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": "logs/backend/django_error.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}
