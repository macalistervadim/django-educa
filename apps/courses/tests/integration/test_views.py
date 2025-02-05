from http import HTTPStatus
from typing import Any

from django.contrib.auth.models import Permission, User
from django.test import TestCase
from django.urls import reverse

import apps.courses.models as c_models


class TestManageCourseListView(TestCase):
    owner_data: dict[str, str]
    owner: User
    course_data: dict[str, Any]
    course: c_models.Course
    subject: c_models.Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "owner_user",
            "email": "owner@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)
        cls.subject = c_models.Subject.objects.create(title="Python")
        cls.course_data = {
            "owner": cls.owner,
            "subject": cls.subject,
            "title": "Course 1",
            "slug": "course-1",
            "overview": "A brief description.",
        }
        cls.course = c_models.Course.objects.create(**cls.course_data)

        permission = Permission.objects.get(codename="view_course")
        cls.owner.user_permissions.add(permission)

    def test_get_queryset_owner(self) -> None:
        """
        Тест фильтрации курсов по владельцу с проверкой разрешений.
        """
        url = reverse("courses:manage_course_list")
        self.client.force_login(self.owner)
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.course, response.context["course_list"])

    def test_get_queryset_anonymous_user(self) -> None:
        """
        Тест, что анонимный пользователь не имеет доступа (требуется вход).
        """
        self.client.logout()
        url = reverse("courses:manage_course_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)


class TestCourseCreateView(TestCase):
    owner_data: dict[str, str]
    owner: User
    course_data: dict[str, Any]
    subject: c_models.Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "owner_user",
            "email": "owner@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)
        cls.subject = c_models.Subject.objects.create(title="Python")
        cls.course_data = {
            "owner": cls.owner.pk,
            "subject": cls.subject.pk,
            "title": "New Course",
            "slug": "new-course",
            "overview": "This is a new course.",
        }
        permission = Permission.objects.get(codename="add_course")
        cls.owner.user_permissions.add(permission)

    def test_create_course(self) -> None:
        """
        Тест создания курса с правильными разрешениями.
        """
        url = reverse("courses:course_create")
        self.client.force_login(self.owner)
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertTrue(c_models.Course.objects.filter(
            owner=self.owner, title="New Course").exists())

    def test_create_course_anonymous(self) -> None:
        """
        Тест, что анонимный пользователь не может создать курс.
        """
        self.client.logout()
        url = reverse("courses:course_create")
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_create_course_no_permission(self) -> None:
        """
        Тест, что пользователь без нужных разрешений не может создать курс.
        """
        no_permission_user = User.objects.create_user(
            username="no_permission_user",
            email="no_permission@mail.ru",
        )
        self.client.force_login(no_permission_user)
        url = reverse("courses:course_create")
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, 403)


class TestCourseUpdateView(TestCase):
    owner_data: dict[str, str]
    owner: User
    course: c_models.Course
    updated_course_data: dict[str, Any]
    subject: c_models.Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "owner_user",
            "email": "owner@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.subject = c_models.Subject.objects.create(title="Python")

        cls.course = c_models.Course.objects.create(
            owner=cls.owner,
            subject=cls.subject,
            title="Old Course",
            slug="old-course",
            overview="Old description.",
        )

        cls.updated_course_data = {
            "subject": cls.subject.pk,
            "title": "Updated Course",
            "slug": "updated-course",
            "overview": "Updated description.",
        }
        permission = Permission.objects.get(codename="change_course")
        cls.owner.user_permissions.add(permission)

    def test_update_course(self) -> None:
        """
        Тест обновления курса с правильными разрешениями.
        """
        url = reverse("courses:course_edit", args=[self.course.pk])
        self.client.force_login(self.owner)
        response = self.client.post(url, self.updated_course_data)
        self.course.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(self.course.title, "Updated Course")

    def test_update_course_anonymous(self) -> None:
        """
        Тест, что анонимный пользователь не может обновить курс.
        """
        self.client.logout()
        url = reverse("courses:course_edit", args=[self.course.pk])
        response = self.client.post(url, self.updated_course_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_update_course_no_permission(self) -> None:
        """
        Тест, что пользователь без нужных разрешений не может обновить курс.
        """
        no_permission_user = User.objects.create_user(
            username="no_permission_user",
            email="no_permission@mail.ru",
        )
        self.client.force_login(no_permission_user)
        url = reverse("courses:course_edit", args=[self.course.pk])
        response = self.client.post(url, self.updated_course_data)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestCourseDeleteView(TestCase):
    owner_data: dict[str, str]
    owner: User
    course: c_models.Course
    subject: c_models.Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "owner_user",
            "email": "owner@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.subject = c_models.Subject.objects.create(title="Python")

        cls.course = c_models.Course.objects.create(
            owner=cls.owner,
            subject=cls.subject,
            title="Course to delete",
            slug="course-to-delete",
            overview="Course description.",
        )

        permission = Permission.objects.get(codename="delete_course")
        cls.owner.user_permissions.add(permission)

    def test_delete_course(self) -> None:
        """
        Тест удаления курса с правильными разрешениями.
        """
        url = reverse("courses:course_delete", args=[self.course.pk])
        self.client.force_login(self.owner)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertFalse(c_models.Course.objects.filter(
            pk=self.course.pk).exists())

    def test_delete_course_anonymous(self) -> None:
        """
        Тест, что анонимный пользователь не может удалить курс.
        """
        self.client.logout()
        url = reverse("courses:course_delete", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_delete_course_no_permission(self) -> None:
        """
        Тест, что пользователь без нужных разрешений
        не может удалить курс.
        """
        no_permission_user = User.objects.create_user(
            username="no_permission_user", email="no_permission@mail.ru")
        self.client.force_login(no_permission_user)
        url = reverse("courses:course_delete", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)
