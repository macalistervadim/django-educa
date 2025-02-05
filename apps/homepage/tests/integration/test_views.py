from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class TestHomepageView(TestCase):
    def test_homepage_get(self) -> None:
        """
        Тестирование GET запроса к главной странице
        """
        response = self.client.get(reverse("homepage:homepage"))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, "homepage/homepage.html")

    def test_homepage_post(self) -> None:
        """
        Тестирование POST запроса к главной странице
        """
        response = self.client.post(reverse("homepage:homepage"))
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)
