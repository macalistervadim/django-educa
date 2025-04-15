from django.contrib import admin
from unfold.admin import ModelAdmin

from backend.apps.feedback.models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(ModelAdmin):
    list_display = (
        "email",
        "subject",
        "created_at",
    )
    search_fields = ("email", "created_at")
    list_filter = ("created_at", "subject")
    ordering = ("-created_at",)
