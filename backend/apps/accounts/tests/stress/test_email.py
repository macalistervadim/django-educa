import os

import django
from django.urls import reverse
from locust import HttpUser, between, task

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "backend.config.settings.development",
)
django.setup()


class EmailLoadTestUser(HttpUser):
    wait_time = between(1, 2)  # type: ignore

    def on_start(self) -> None:
        response = self.client.get("/")
        self.csrf_token = response.cookies.get("csrftoken", "")

    @task
    def send_email(self) -> None:
        """Отправляем запрос для сброса пароля,
        который вызывает задачу Celery"""
        url = reverse("accounts:password_reset")
        headers = {"X-CSRFToken": self.csrf_token}

        # TODO: прикрутить фикстуры с
        #  реальными почтами юзеров и убрать этот хардкод
        response = self.client.post(
            url,
            {"email": "startsevvadim2007@gmail.com"},
            headers=headers,
        )

        if response.status_code == 200:
            print("Email отправлен для startsevvadim2007@gmail.com")
        else:
            print("Ошибка при отправке email для startsevvadim2007@gmail.com")
