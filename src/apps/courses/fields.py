from typing import Any, cast

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class OrderField(models.PositiveIntegerField):
    """
    Поле для автоматического определения порядка объектов.
    """

    def __init__(
        self,
        for_fields: Any = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        self.for_fields = for_fields
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance: models.Model, add: bool) -> int:
        if getattr(model_instance, self.attname) is None:
            try:
                qs = self.model._default_manager.all()
                if self.for_fields:
                    query = {
                        field: getattr(model_instance, field)
                        for field in self.for_fields
                    }
                    qs = qs.filter(**query)
                last_item = cast(
                    models.Model,
                    qs.latest(self.attname),
                )
                value = last_item.order + 1  # type: ignore
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super().pre_save(model_instance, add)
