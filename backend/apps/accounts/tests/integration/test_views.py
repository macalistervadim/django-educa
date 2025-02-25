from http import HTTPStatus

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AccountsViewsTests(TestCase):
    user_data: dict[str, str]
    user: User

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Создаём тестовые данные, которые будут использоваться во всех тестах.
        """
        cls.user_data = {
            "username": "testuser",
            "password": "testpass123",
        }
        cls.user = User.objects.create_user(**cls.user_data)

    def test_login_view_get(self) -> None:
        """
        Тест GET-запроса к странице входа.
        """
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "accounts/registration/login.html")

    def test_login_view_post_success(self) -> None:
        """
        Тест успешного POST-запроса к странице входа.
        """
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
        )

    def test_login_view_post_failure(self) -> None:
        """
        Тест неудачного POST-запроса к странице входа.
        """
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "wronguser",
                "password": "wrongpass",
            },
        )
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )
        self.assertTemplateUsed(response, "accounts/registration/login.html")

    def test_logout_view_get(self) -> None:
        """
        Тест GET-запроса к странице выхода.
        """
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_logout_view_post(self) -> None:
        """
        Тест POST-запроса к странице выхода.
        """
        self.client.login(
            username=self.user_data["username"],
            password=self.user_data["password"],
        )
        response = self.client.post(reverse("accounts:logout"))
        self.assertEqual(
            response.status_code,
            HTTPStatus.OK,
        )

    def test_logout_view_unauthenticated(self) -> None:
        """
        Тест страницы выхода для неаутентифицированного пользователя.
        """
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
