from django.db.models import QuerySet
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.courses.models import Course
from apps.courses.views.mixins.owner import OwnerCourseEditMixin


class ManageCourseListView(ListView):  # TODO: test
    model = Course
    template_name = "courses/manage/course/list.html"

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):  # TODO: test
    pass


class CouseUpdateView(OwnerCourseEditMixin, UpdateView):  # TODO: test
    pass


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):  # TODO: test
    pass
