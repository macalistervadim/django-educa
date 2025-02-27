from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from backend.apps.courses.models import Course, Subject


class CourseListView(TemplateResponseMixin, View):  # TODO: test
    model = Course
    template_name = "courses/course/list.html"

    def get(
        self, request: HttpRequest, subject: Subject | None = None,
    ) -> HttpResponse:
        subjects = Subject.objects.annotate(
            total_courses=Count("courses"),
        )
        courses = Course.objects.annotate(
            total_modules=Count("modules"),
        )

        if subject:
            subject = get_object_or_404(Subject, slug=subject)
            courses = courses.filter(subject=subject)

        return self.render_to_response(
            {
                "subjects": subjects,
                "subject": subject,
                "courses": courses,
            },
        )
