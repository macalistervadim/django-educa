import os

from celery import Celery

settings_module = os.getenv(
    "DJANGO_SETTINGS_MODULE",
    "backend.config.settings.development",
)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)

app = Celery("celery_worker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
