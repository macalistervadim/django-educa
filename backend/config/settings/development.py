from typing import Any

from backend.config.settings.base import *  # noqa: F403

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

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

