from django.test import TestCase
from django.urls import resolve, reverse

from backend.apps.feedback.views import FeedbackView


class FeedbackURLTests(TestCase):
    def test_feedback_url(self) -> None:
        url = reverse("feedback:feedback")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            FeedbackView.as_view().__name__,
        )

        self.assertTemplateUsed(response, "feedback/feedback.html")
