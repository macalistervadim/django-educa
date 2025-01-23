from django.contrib.auth.models import User
from django.db import models


class ItemBase(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="%(class)s_related",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"owner={self.owner!r}, "
            f"title={self.title!r}, "
            f"created={self.created!r}, "
            f"updated={self.updated!r}"
        )


class Text(ItemBase):
    content = models.TextField()

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"{base_repr}, content={self.content!r})"


class File(ItemBase):
    file = models.FileField(upload_to="files")

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"{base_repr}, file={self.file!r})"


class Image(ItemBase):
    file = models.FileField(upload_to="images")

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"{base_repr}, file={self.file!r})"


class Video(ItemBase):
    url = models.URLField()

    def __repr__(self) -> str:
        base_repr = super().__repr__()
        return f"{base_repr}, url={self.url!r})"
