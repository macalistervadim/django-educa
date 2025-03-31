from http import HTTPStatus
from typing import Any

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from backend.apps.courses.models import Course
from backend.сommon.tests.base_setup_data import BaseSetUpData


class TestCourseChatRoomView(BaseSetUpData, TestCase):
    user: Any
    joined_user: Any
    course: Course

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        get_user_model().objects.filter(username="user").prefetch_related(
            "courses_joined",
        ).delete()

        cls.user = get_user_model().objects.create(
            username="artem",
            password="artem",
        )
        cls.joined_user = get_user_model().objects.create(
            username="artem_joined",
            password="testpassword",
        )

        cls.course.students.add(cls.joined_user)

    def tearDown(self) -> None:
        self.course.students.clear()
        self.course.delete()
        self.subject.delete()
        self.owner.delete()
        self.user.delete()
        self.joined_user.delete()

    def test_course_chat_room_authenticated(self) -> None:
        """Тест авторизованного пользователя, который зачислен на курс"""
        self.client.login(username="artem_joined", password="testpassword")

        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_course_chat_room_not_authenticated(self) -> None:
        """Тест для неавторизованного пользователя
        — должен редиректить на логин"""
        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)  # 302
        self.assertRedirects(
            response,
            f"/accounts/login/?next={
                reverse('chat:course_chat_room', args=[self.course.id])
            }",
        )

    def test_course_chat_room_invalid_course_id(self) -> None:
        """Тест для несуществующего курса"""
        self.client.login(username="artem_joined", password="testpassword")

        invalid_course_id = 999
        response = self.client.get(
            reverse("chat:course_chat_room", args=[invalid_course_id]),
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_course_chat_room_not_joined_course(self) -> None:
        """Тест авторизованного пользователя, который НЕ зачислен курс"""
        self.client.login(
            username="artem",
            password="artem",
        )

        response = self.client.get(
            reverse("chat:course_chat_room", args=[self.course.id]),
        )

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
