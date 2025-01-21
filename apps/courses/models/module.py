from django.db import models

from apps.courses.models.course import Course


class Module(models.Model):
    course = models.ForeignKey(
        Course,
        related_name="modules",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.title}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"course={self.course!r}, "
            f"title={self.title!r}, "
            f"description={self.description!r})"
        )
