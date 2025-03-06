from typing import Any
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from django.urls import reverse

from backend.apps.chat.views.course_chat_room import course_chat_room
from backend.сommon.tests.base_setup_data import BaseSetUpData


class TestCourseChatRoomView(BaseSetUpData, TestCase):
    def setUp(self) -> None:
        super().setUpTestData()
        self.user = get_user_model().objects.create_user(
            username="user",
            password="testpassword",
        )

    def test_course_chat_room_authenticated(self) -> None:
        self.client.login(username="user", password="testpassword")

        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            "Python",
        )

    def test_course_chat_room_not_authenticated(self) -> None:
        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, 403)

    def test_course_chat_room_invalid_course_id(self) -> None:
        self.client.login(username="user", password="testpassword")

        invalid_course_id = 999
        response = self.client.get(
            reverse("chat:course_chat_room", args=[invalid_course_id]),
        )

        self.assertEqual(response.status_code, 403)

    def test_course_chat_room_not_joined_course(self) -> None:
        get_user_model().objects.create_user(
            username="anotheruser",
            password="anotherpassword",
        )
        self.client.login(username="anotheruser", password="anotherpassword")

        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, 403)

    @patch("backend.apps.chat.views.render")
    def test_view_function_return_type(self, mock_render: Any) -> None:
        request = HttpRequest()
        request.user = self.user

        self.client.force_login(self.user)

        mock_render.return_value = HttpResponse("test response")

        response = course_chat_room(request, self.course.id)

        mock_render.assert_called_with(
            request,
            "chat/room.html",
            {"course": self.course},
        )

        self.assertEqual(response.content, b"test response")
