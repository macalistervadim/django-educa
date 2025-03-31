from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import FormView

from backend.apps.students.forms import CourseEnrollForm


class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm

    def form_valid(self, form: CourseEnrollForm) -> HttpResponse:
        self.course = form.cleaned_data["course"]
        self.course.students.add(self.request.user)
        return super().form_valid(form)

    def get_success_url(self) -> str:
        if self.course:
            return reverse_lazy(
                "students:student_course_detail",
                args=[self.course.id],
            )
        return reverse_lazy("students:course_list")
