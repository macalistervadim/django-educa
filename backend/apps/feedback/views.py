from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import FormView

from backend.apps.feedback.forms import FeedbackForm
from backend.apps.feedback.models import Feedback


class FeedbackView(FormView):
    form_class = FeedbackForm
    model = Feedback
    template_name = "feedback/feedback.html"
    success_url = reverse_lazy("feedback:feedback")

    def form_valid(self, form: FeedbackForm) -> HttpResponse:
        form.save()
        return super().form_valid(form)
