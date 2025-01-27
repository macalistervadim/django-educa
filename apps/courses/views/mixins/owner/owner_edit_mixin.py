from django import forms
from django.http import HttpRequest, HttpResponse


class OwnerEditMixin:
    """
    Миксин для привязки текущего пользователя к объекту формы.
    """

    request: HttpRequest

    def form_valid(self, form: forms.ModelForm) -> HttpResponse:
        form.instance.owner = self.request.user
        return super().form_valid(form)  # type: ignore
