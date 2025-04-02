from django.test import TestCase

from backend.apps.feedback.models import Feedback


class TestFeedbackModel(TestCase):
    data: dict[str, str]
    feedback: Feedback

    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {
            "email": "test@mail.ru",
            "subject": "testSubject",
            "message": "testMessage",
        }
        cls.feedback = Feedback.objects.create(**cls.data)

    def test_create_feedback_success(self) -> None:
        """
        Тестирование создания модели Feedback
        """
        feedback = Feedback.objects.first()
        self.assertEqual(Feedback.objects.count(), 1)
        if feedback:
            self.assertEqual(feedback.email, self.data["email"])
            self.assertEqual(feedback.subject, self.data["subject"])
            self.assertEqual(feedback.message, self.data["message"])

    def test_str_method(self) -> None:
        """
        Тестирование __str__ метода модели Feedback
        """
        self.assertEqual(
            str(self.feedback),
            f"Feedback from {self.data['email']} with subject: "
            f"{self.data['subject']}",
        )

    def test_repr_method(self) -> None:
        """
        Тестирование __repr__ метода модели Feedback
        """
        self.assertEqual(
            repr(self.feedback),
            "Feedback("
            f"email={self.feedback.email!r}, "
            f"subject={self.feedback.subject!r}, "
            f"message={self.feedback.message!r}, "
            f"created_at={self.feedback.created_at!r})",
        )
