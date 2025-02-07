from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from src.apps.courses.models import Module


class ModuleContentListView(TemplateResponseMixin, View):  # TODO: test
    module: Module
    template_name = "courses/manage/module/content_list.html"

    def get(self, request: HttpRequest, module_id: int) -> HttpResponseBase:
        module = get_object_or_404(
            Module,
            id=module_id,
            course__owner=request.user,
        )
        return self.render_to_response({"module": module})
