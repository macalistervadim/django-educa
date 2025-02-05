from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import resolve, reverse

import apps.courses.views.manage_course as c_views


class CoursesUrlsTests(TestCase):
    owner: User
    owner_data: dict[str, str]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "owner_user",
            "email": "owner@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        permissions = [
            "view_course",
            "add_course",
            "change_course",
            "delete_course",
        ]
        permissions_to_add = [
            Permission.objects.get(codename=perm) for perm in permissions]
        cls.owner.user_permissions.add(*permissions_to_add)

    def setUp(self) -> None:
        self.client.force_login(self.owner)

    def test_manage_course_list_url(self) -> None:
        """
        Тест доступности GET запроса к урлу списка курсов
        """
        url = reverse("courses:manage_course_list")
        self.assertEqual(url, reverse("courses:manage_course_list"))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_views.ManageCourseListView.as_view().__name__)

        response = self.client.get(url)
        self.assertTemplateUsed(response, "courses/manage/course/list.html")

    def test_course_create_url(self) -> None:
        """
        Тест доступности GET запроса к урлу создания курса
        """
        url = reverse("courses:course_create")
        self.assertEqual(url, reverse("courses:course_create"))

        resolved = resolve(url)
        self.assertEqual(resolved.func.__name__,
            c_views.CourseCreateView.as_view().__name__)

        response = self.client.get(url)
        self.assertTemplateUsed(response, "courses/manage/course/form.html")

    def test_course_edit_url(self) -> None:
        """
        Тест недоступности GET запроса к урлу изменения курса,
        так как не был передан корректный курс в урл
        """
        url = reverse("courses:course_edit", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_course_delete_url(self) -> None:
        """
        Тест недоступности GET запроса к урлу удаления курса,
        так как не был передан корректный курс в урл
        """
        url = reverse("courses:course_delete", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
