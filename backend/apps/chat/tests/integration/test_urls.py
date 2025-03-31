from django.test import TestCase
from django.urls import resolve, reverse

from backend.apps.chat.views.course_chat_room import course_chat_room


class TestCourseChatRoomUrls(TestCase):
    def test_valid_url(self) -> None:
        url = reverse("chat:course_chat_room", args=[1])
        self.assertEqual(url, reverse("chat:course_chat_room", args=[1]))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            course_chat_room.__name__,
        )
