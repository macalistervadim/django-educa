from django.contrib.auth.models import User
from django.db import models

from apps.courses.models.subject import Subject


class Course(models.Model):
    owner = models.ForeignKey(
        User,
        related_name="courses_created",
        on_delete=models.CASCADE,
    )
    subject = models.ForeignKey(
        Subject,
        related_name="courses",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.owner!r}, "
            f"{self.subject!r}, "
            f"{self.title!r}, "
            f"{self.slug!r}, "
            f"{self.overview!r}, "
            f"{self.created!r})"
        )  # todo: исправить
