from django.forms.models import BaseInlineFormSet, inlineformset_factory

from src.apps.courses.models import Course, Module

ModuleFormSet: type[BaseInlineFormSet] = inlineformset_factory(
    Course,
    Module,
    fields=["title", "description"],
    extra=2,
    can_delete=True,
)
