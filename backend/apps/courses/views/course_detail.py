from django.views.generic.detail import DetailView

from backend.apps.courses.models import Course


class CourseDetailView(DetailView):  # TODO: test
    model = Course
    template_name = "courses/course/detail.html"
