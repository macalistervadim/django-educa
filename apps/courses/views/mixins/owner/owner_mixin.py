from django.db.models import QuerySet
from django.http import HttpRequest


class OwnerMixin:
    """
    Миксин для фильтрации объектов по владельцу (owner).
    """

    request: HttpRequest

    def get_queryset(self) -> QuerySet:
        qs = super().get_queryset()  # type: ignore
        return qs.filter(owner=self.request.user)
