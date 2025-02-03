from django import forms
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy

from apps.courses.models import Course


class OwnerEditMixin:
    """
    Миксин для привязки текущего пользователя к объекту формы.
    """

    request: HttpRequest

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)  # type: ignore


class OwnerMixin:
    """
    Миксин для фильтрации объектов по владельцу (owner).
    """

    request: HttpRequest

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()  # type: ignore
        return qs.filter(owner=self.request.user)


class OwnerCourseMixin(OwnerMixin):
    """
    Миксин для предоставления общей функциональности для представлений,
    которые обрабатывают объекты Course, принадлежащие конкретному пользователю
    """

    model = Course
    fields = [
        Course.subject.field.name,
        Course.slug.field.name,
        Course.overview.field.name,
    ]
    success_url = reverse_lazy("courses:manage_course_list")


class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    """
    Миксин для редактирования курсов, принадлежащих конкретному пользователю.
    """

    template_name = "courses/manage/course/form.html"
