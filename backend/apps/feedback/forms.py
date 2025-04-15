from django.forms import ModelForm

from backend.apps.feedback.models import Feedback


class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ["email", "subject", "message"]
