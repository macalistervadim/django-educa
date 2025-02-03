from django.db.models import QuerySet
from django.http import Http404
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.courses.models import Course
from apps.courses.views.mixins.owners_mixins import OwnerCourseEditMixin


class ManageCourseListView(ListView):
    model = Course
    template_name = "courses/manage/course/list.html"
    permission_required = "courses.view_course"

    def get_queryset(self) -> QuerySet:
        if self.request.user.is_anonymous:
            raise Http404("Access denied")

        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)


class CourseCreateView(OwnerCourseEditMixin, CreateView):
    model = Course
    template_name = "courses/manage/course/form.html"
    permission_required = "courses.add_course"
    fields = [
        Course.subject.field.name,
        Course.title.field.name,
        Course.slug.field.name,
        Course.overview.field.name,
    ]


class CourseUpdateView(OwnerCourseEditMixin, UpdateView):
    model = Course
    template_name = "courses/manage/course/form.html"
    permission_required = "courses.change_course"
    fields = [
        Course.subject.field.name,
        Course.title.field.name,
        Course.slug.field.name,
        Course.overview.field.name,
    ]


class CourseDeleteView(OwnerCourseEditMixin, DeleteView):
    model = Course
    template_name = "courses/manage/course/delete.html"
    permission_required = "courses.delete_course"
    object = Course
