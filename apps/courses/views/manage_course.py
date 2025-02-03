from typing import Any

from django.db.models import QuerySet
from django.forms.models import BaseInlineFormSet
from django.http import Http404, HttpRequest, HttpResponse, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.views import View
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from apps.courses.forms import ModuleFormSet
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


class CourseModuleUpdateView(TemplateResponseMixin, View):  # TODO: TEST
    template_name = "courses/manage/module/formset.html"
    course = None

    def get_queryset(
        self, data: dict[str, Any] | None = None,
    ) -> BaseInlineFormSet:
        return ModuleFormSet(
            instance=self.course, data=data,
        )

    def dispatch(self, request: HttpRequest, pk: int) -> HttpResponseBase:
        self.course = get_object_or_404(
            Course, id=pk, owner=request.user,
        )
        return super().dispatch(request, pk)

    def get(
        self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:
        formset = self.get_queryset()
        return self.render_to_response({"course": self.course,
                                        "formset": formset})

    def post(
        self, request: HttpRequest, *args: Any, **kwargs: Any,
    ) -> HttpResponse:
        formset = self.get_queryset(data=request.POST)
        if formset.is_valid():
            formset.save()
            return redirect("courses:manage_course_list")
        return self.render_to_response({"course": self.course,
                                        "formset": formset})

