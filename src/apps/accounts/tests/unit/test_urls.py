from django.contrib.auth import views as auth_views
from django.test import TestCase
from django.urls import resolve, reverse


class UsersUrlsTests(TestCase):
    def test_login_url(self) -> None:
        url = reverse("accounts:login")
        self.assertEqual(url, reverse("accounts:login"))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            auth_views.LoginView.as_view().__name__,
        )

    def test_logout_url(self) -> None:
        url = reverse("accounts:logout")
        self.assertEqual(url, reverse("accounts:logout"))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            auth_views.LogoutView.as_view().__name__,
        )
