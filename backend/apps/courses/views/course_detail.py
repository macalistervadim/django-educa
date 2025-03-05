from typing import Any

from django.views.generic.detail import DetailView

from backend.apps.courses.models import Course
from backend.apps.students.forms import CourseEnrollForm


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course/detail.html"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["enroll_form"] = CourseEnrollForm(
            initial={"course": self.object},
        )
        return context
