from django.urls import path

from backend.apps.chat.views.course_chat_room import course_char_room

app_name = "chat"


urlpatterns = [
    path(
        "room/<int:course_id>/",
        course_char_room,
        name="course_chat_room",
    ),
]
