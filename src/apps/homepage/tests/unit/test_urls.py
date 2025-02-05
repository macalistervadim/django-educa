from django.test import TestCase
from django.urls import resolve, reverse

import apps.homepage.views.homepage as h_views


class TestHomepageUrls(TestCase):
    def test_homepage_url(self) -> None:
        url = reverse("homepage:homepage")
        self.assertEqual(url, reverse("homepage:homepage"))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            h_views.HomepageView.as_view().__name__,
        )
