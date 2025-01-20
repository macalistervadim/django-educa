from django.db import models


class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(" f"{self.title!r}, " f"{self.slug!r})"
        )  # TODO: исправить
