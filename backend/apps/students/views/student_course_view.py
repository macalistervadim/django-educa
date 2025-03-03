from typing import Any

from django.db.models import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from backend.apps.courses.models import Course


class StudentCourseListView(ListView):  # TODO: test
    model = Course
    template_name = "students/course/list.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(
        self,
        *,
        object_list: None | Any = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["courses"] = self.get_queryset()
        return context


class StudentCourseDetailView(DetailView):  # TODO: test
    model = Course
    template_name = "students/course/detail.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])

    def get_context_data(self, **kwargs: dict[str, Any]) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        course = self.get_object()
        if "module_id" in self.kwargs:
            context["module"] = course.modules.get(
                id=self.kwargs["module_id"],
            )
        else:
            context["module"] = course.modules.all()[0]
        return context
