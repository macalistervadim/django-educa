from django.urls import reverse_lazy

from apps.courses.models import Course
from apps.courses.views.mixins.owner import OwnerMixin


class OwnerCourseMixin(OwnerMixin):
    """
    Миксин для предоставления общей функциональности для представлений,
    которые обрабатывают объекты Course, принадлежащие конкретному пользователю
    """

    model = Course
    fields = [
        Course.subject.field.name,
        Course.title.field.name,
        Course.slug.field.name,
        Course.overview.field.name,
    ]
    success_url = reverse_lazy("courses:manage_course_list")
