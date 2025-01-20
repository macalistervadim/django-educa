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
            f"owner={self.owner!r}, "
            f"subject={self.subject!r}, "
            f"title={self.title!r}, "
            f"slug={self.slug!r}, "
            f"overview={self.overview!r}, "
            f"created={self.created!r})"
        )
