from typing import Any

from django import template

register = template.Library()


@register.filter
def model_name(obj: Any) -> str | None:
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
