from django.forms.models import BaseInlineFormSet, inlineformset_factory

from apps.courses.models import Course, Module

ModuleFormSet: type[BaseInlineFormSet] = inlineformset_factory(
    Course,  # TODO: test
    Module,
    fields=["title", "description"],
    extra=2,
    can_delete=True,
)
