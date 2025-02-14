from http import HTTPStatus

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import resolve, reverse

import src.apps.courses.models as c_models
import src.apps.courses.views.content_create_update as c_content_manage_views
import src.apps.courses.views.manage_course as c_manage_course_views
import src.apps.courses.views.module_content_list as c_content_list_views


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
            Permission.objects.get(codename=perm) for perm in permissions
        ]
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
            c_manage_course_views.ManageCourseListView.as_view().__name__,
        )

        response = self.client.get(url)
        self.assertTemplateUsed(response, "courses/manage/course/list.html")

    def test_course_create_url(self) -> None:
        """
        Тест доступности GET запроса к урлу создания курса
        """
        url = reverse("courses:course_create")
        self.assertEqual(url, reverse("courses:course_create"))

        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_manage_course_views.CourseCreateView.as_view().__name__,
        )

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


class ModuleContentUrlsTests(TestCase):
    user: User
    module: c_models.Module
    course: c_models.Course
    user_data: dict[str, str]
    subject: c_models.Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "username": "test_user1",
            "email": "user1@mail.com",
            "password": "password123",
        }
        cls.user = User.objects.create_user(**cls.user_data)
        permissions_codenames = [
            "delete_course",
            "change_course",
            "add_course",
        ]
        permissions = Permission.objects.filter(
            codename__in=permissions_codenames,
        )
        cls.user.user_permissions.add(*permissions)

        cls.subject = c_models.Subject.objects.create(title="Java")

        cls.course = c_models.Course.objects.create(
            owner=cls.user,
            subject=cls.subject,
            title="Course to delete123",
            slug="course-to-delete123",
            overview="Course description123.",
        )

        cls.module = c_models.Module.objects.create(
            course=cls.course,
            title="Test Module123",
            description="Test Description123",
        )

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_module_content_create_url(self) -> None:
        """
        Тестирование доступности GET запроса к ContentCreateUpdateView
        """
        url = reverse("courses:module_content_create", args=[1, "video"])
        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_content_manage_views.ContentCreateUpdateView.as_view().__name__,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_module_content_update_url(self) -> None:
        """
        Тестирование доступности GET запроса к ContentCreateUpdateView
        """
        url = reverse("courses:module_content_update", args=[1, "video", 1])
        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_content_manage_views.ContentCreateUpdateView.as_view().__name__,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_module_content_delete_url(self) -> None:
        """
        Тестирование доступности GET запроса к ContentDeleteView
        """
        url = reverse("courses:module_content_delete", args=[1])
        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_content_manage_views.ContentDeleteView.as_view().__name__,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.METHOD_NOT_ALLOWED)

    def test_module_content_list_url(self) -> None:
        """
        Тестирование доступности GET запроса к ModuleContentListView
        """
        url = reverse("courses:module_content_list", args=[1])
        resolved = resolve(url)
        self.assertEqual(
            resolved.func.__name__,
            c_content_list_views.ModuleContentListView.as_view().__name__,
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
