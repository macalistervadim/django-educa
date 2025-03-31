from typing import Any

import dotenv

from backend.config.settings.base import *  # noqa: F403

dotenv.load_dotenv()

DEBUG = True

INSTALLED_APPS += [
    "debug_toolbar",
]

MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")

INTERNAL_IPS = ["127.0.0.1", "localhost", "0.0.0.0", "host.docker.internal"]


def show_toolbar(request: Any) -> Any:
    from django.conf import settings

    return settings.DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    "IS_RUNNING_TESTS": False,
}

TEMPLATES[0]["OPTIONS"]["debug"] = True  # type: ignore

INSTALLED_APPS += ["corsheaders"]
MIDDLEWARE.insert(1, "corsheaders.middleware.CorsMiddleware")
CORS_ALLOWED_ORIGINS = load_list(
    "DJANGO_CORS_ALLOWED_ORIGINS",
    ["http://localhost:3000"],
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    },
}

# LOGGING = {
#     "version": 1,
#     "disable_existing_loggers": False,
#     "formatters": {
#         "verbose": {
#             "format": "{levelname} {asctime} {module} {message}",
#             "style": "{",
#         },
#         "simple": {
#             "format": "{levelname} {message}",
#             "style": "{",
#         },
#     },
#     "handlers": {
#         "console": {
#             "level": "DEBUG",
#             "class": "logging.StreamHandler",
#             "formatter": "verbose",
#         },
#     },
#     "loggers": {
#         "django": {
#             "handlers": ["console"],
#             "level": "DEBUG",
#             "propagate": True,
#         },
#     },
# }
