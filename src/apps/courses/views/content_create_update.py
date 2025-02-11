from typing import Any

from django.apps import apps
from django.db import models
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin

from src.apps.courses.models import (
    Content,
    Module,
)
from src.apps.courses.views.mixins.content_owner import ContentOwnerMixin


class ContentCreateUpdateView(
    ContentOwnerMixin,
    TemplateResponseMixin,
    View,
):
    content: Content
    module: Module | None = None
    model: type[models.Model] | None = None
    obj: models.Model | None = None
    template_name = "courses/manage/content/form.html"

    def get_model(self, model_name: str) -> type[models.Model] | None:
        if model_name in ["text", "video", "image", "file"]:
            return apps.get_model(app_label="courses", model_name=model_name)
        return None

    def get_form(
        self,
        model: type[models.Model],
        *args: Any,
        **kwargs: Any,
    ) -> ModelForm:
        form_class = modelform_factory(
            model,
            exclude=["owner", "order", "created", "updated"],
        )
        return form_class(*args, **kwargs)

    def dispatch(
        self,
        request: HttpRequest,
        module_id: int,
        model_name: str,
        pk: int | None = None,
    ) -> HttpResponseBase:
        self.module = get_object_or_404(Module, id=module_id)
        self.model = self.get_model(model_name)
        if pk and self.model:
            self.obj = get_object_or_404(self.model, id=pk, owner=request.user)
        return super().dispatch(request, module_id, model_name, pk)

    def get(
        self,
        request: HttpRequest,
        module_id: int,
        model_name: str,
        pk: int | None = None,
    ) -> HttpResponseBase:
        if self.model is None:
            return self.render_to_response({"form": None, "object": self.obj})
        form = self.get_form(self.model, instance=self.obj)
        return self.render_to_response({"form": form, "object": self.obj})

    def post(
        self,
        request: HttpRequest,
        module_id: int,
        model_name: str,
        pk: int | None = None,
    ) -> HttpResponseBase:
        if self.model is None or self.module is None:
            return self.render_to_response({"form": None, "object": self.obj})

        form = self.get_form(
            self.model,
            instance=self.obj,
            data=request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner = request.user
            obj.save()
            if not pk:
                Content.objects.create(module=self.module, item=obj)
            return redirect(
                "courses:module_content_list",
                self.module.pk if self.module else 0,
            )
        return self.render_to_response({"form": form, "object": self.obj})


class ContentDeleteView(ContentOwnerMixin, View):
    def post(
        self,
        request: HttpRequest,
        pk: int,
    ) -> HttpResponseBase:
        content = get_object_or_404(
            Content,
            id=pk,
            module__course__owner=request.user,
        )
        module = content.module
        if content.item:
            content.item.delete()
        content.delete()
        return redirect(
            "courses:module_content_list",
            module.pk,
        )
