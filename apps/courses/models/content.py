from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apps.courses.fields import OrderField
from apps.courses.models.module import Module


class Content(models.Model):  # TODO: test this
    module = models.ForeignKey(
        Module,
        related_name="contents",
        on_delete=models.CASCADE,
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            "model__in": (
                "text",
                "video",
                "image",
                "file",
            ),
        },
    )
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey("content_type", "object_id")
    order = OrderField(for_fields=["module"], blank=True)

    class Meta:
        ordering = ["order"]  # TODO: test this

    def __str__(self) -> str:
        return f"{self.object_id} - {self.item}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"module={self.module!r}, "
            f"content_type={self.content_type!r}, "
            f"object_id={self.object_id!r}, "
            f"item={self.item!r}, "
            f"order={self.order!r})"
        )
