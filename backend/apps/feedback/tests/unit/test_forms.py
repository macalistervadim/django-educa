from django.test import TestCase

from backend.apps.feedback.forms import FeedbackForm


class TestFeedbackForm(TestCase):
    def test_valid_form(self) -> None:
        data = {
            "email": "test@mail.ru",
            "subject": "anySubject",
            "message": "testMessage",
        }
        form = FeedbackForm(data=data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["email"], "test@mail.ru")
        self.assertEqual(form.cleaned_data["subject"], "anySubject")
        self.assertEqual(form.cleaned_data["message"], "testMessage")

    def test_invalid_form(self) -> None:
        data = {
            "subject": "anySubject",
            "message": "testMessage",
        }

        form = FeedbackForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertFormError(
            form=form,  # type: ignore
            field="email",
            errors=["This field is required."],
        )
