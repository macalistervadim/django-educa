import os

from django.core.asgi import get_asgi_application

settings_module = os.getenv(
    "DJANGO_SETTINGS_MODULE",
    "src.config.settings.production",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

application = get_asgi_application()
