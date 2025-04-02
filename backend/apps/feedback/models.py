from django.db import models


class Feedback(models.Model):
    email = models.EmailField(max_length=254)
    subject = models.CharField(max_length=100)
    message = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

    def __str__(self) -> str:
        return f"Feedback from {self.email} with subject: {self.subject}"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"email={self.email!r}, "
            f"subject={self.subject!r}, "
            f"message={self.message!r}, "
            f"created_at={self.created_at!r})"
        )
