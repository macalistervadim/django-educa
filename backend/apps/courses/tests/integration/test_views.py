from http import HTTPStatus
from typing import Any

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.urls import reverse

import backend.apps.courses.models as c_models
from backend.сommon.tests.base_setup_data import (
    BaseSetUpData,
    BaseSetUpDataContentClasses,
)


class TestManageCourseListView(BaseSetUpData, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

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


class TestCourseCreateView(BaseSetUpData, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        permission = Permission.objects.get(codename="add_course")
        cls.owner.user_permissions.add(permission)

    def test_create_course(self) -> None:
        """
        Тест создания курса с правильными разрешениями.
        """
        url = reverse("courses:course_create")
        self.client.force_login(self.owner)
        response = self.client.post(url, self.course_data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            c_models.Course.objects.filter(
                owner=self.owner,
                title=self.course.title,
            ).exists(),
        )

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


class TestCourseUpdateView(BaseSetUpData, TestCase):
    updated_course_data: dict[str, Any]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

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


class TestCourseDeleteView(BaseSetUpData, TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

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
        self.assertFalse(
            c_models.Course.objects.filter(pk=self.course.pk).exists(),
        )

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
            username="no_permission_user",
            email="no_permission@mail.ru",
        )
        self.client.force_login(no_permission_user)
        url = reverse("courses:course_delete", args=[self.course.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestContentCreateUpdateView(
    BaseSetUpDataContentClasses,
    TestCase,
):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_get_request_create_content(self) -> None:
        """
        Тест GET-запроса для создания нового контента.
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_create",
            args=[self.module.pk, "text"],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("form", response.context)
        self.assertIsNone(response.context["object"])

    def test_post_request_create_content_valid(self) -> None:
        """
        Тест POST-запроса для создания нового контента с валидными данными.
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_create",
            args=[self.module.pk, "text"],
        )
        data = {"title": "test", "content": "NEW content"}

        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code,
            HTTPStatus.FOUND,
        )

        self.assertEqual(c_models.Content.objects.count(), 2)

    def test_post_request_create_content_invalid(self) -> None:
        """
        Тест POST-запроса с невалидными данными (пустое поле).
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_create",
            args=[self.module.pk, "text"],
        )
        data = {"content": ""}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        form = response.context["form"]
        self.assertFormError(
            form,
            "content",
            "This field is required.",
        )

    def test_get_request_update_content(self) -> None:
        """
        Тест GET-запроса для редактирования существующего контента.
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_update",
            args=[self.module.pk, "text", self.text_content.pk],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("form", response.context)
        self.assertEqual(response.context["object"], self.text_content)

    def test_post_request_update_content_valid(self) -> None:
        """
        Тест POST-запроса для обновления контента с валидными данными.
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_update",
            args=[self.module.pk, "text", self.text_content.pk],
        )
        data = {"title": "test", "content": "Updated content"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.text_content.refresh_from_db()
        self.assertEqual(self.text_content.content, "Updated content")

    def test_get_request_invalid_model(self) -> None:
        """
        Тест GET-запроса с несуществующей моделью.
        """
        self.client.force_login(self.user)
        url = reverse(
            "courses:module_content_create",
            args=[self.module.pk, "invalid_model"],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIsNone(response.context["form"])

    def test_anonymous_user_access(self) -> None:
        """
        Тест, что анонимный пользователь не может получить доступ к
        созданию/редактированию контента.
        """
        url = reverse(
            "courses:module_content_create",
            args=[self.module.pk, "text"],
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)


class TestContentDeleteView(
    BaseSetUpDataContentClasses,
    TestCase,
):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

    def test_post_request_delete_content(self) -> None:
        """
        Тест POST-запроса для удаления контента.
        """
        self.client.force_login(self.user)

        self.assertEqual(c_models.Content.objects.count(), 1)

        url = reverse(
            "courses:module_content_delete",
            args=[self.content.pk],
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        with self.assertRaises(c_models.Content.DoesNotExist):
            self.content.refresh_from_db()

        with self.assertRaises(c_models.Text.DoesNotExist):
            self.text_content.refresh_from_db()

        self.assertEqual(c_models.Content.objects.count(), 0)

    def test_post_request_delete_content_not_owner(self) -> None:
        """
        Тест, что пользователь, не являющийся владельцем,
        не может удалить контент.
        """
        other_user = User.objects.create_user(
            username="other_user",
            email="other@mail.com",
            password="password123",
        )

        self.client.force_login(other_user)

        url = reverse(
            "courses:module_content_delete",
            args=[self.content.pk],
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)

        self.assertEqual(c_models.Content.objects.count(), 1)

    def test_post_request_delete_content_not_authenticated(self) -> None:
        """
        Тест, что неаутентифицированный пользователь не может удалить контент.
        """
        url = reverse(
            "courses:module_content_delete",
            args=[self.content.pk],
        )

        response = self.client.post(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        self.assertEqual(c_models.Content.objects.count(), 1)


class TestModuleContentListView(BaseSetUpData, TestCase):
    module: c_models.Module

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        permissions_codenames = [
            "delete_course",
            "change_course",
            "add_course",
        ]
        permissions = Permission.objects.filter(
            codename__in=permissions_codenames,
        )
        cls.owner.user_permissions.add(*permissions)

        cls.module = c_models.Module.objects.create(
            course=cls.course,
            title="Test Module123",
            description="Test Description123",
        )

    def test_get_request_valid(self) -> None:
        """
        Тестирование GET запроса на получение контента для владельца курса.
        """
        self.client.force_login(self.owner)
        url = reverse("courses:module_content_list", args=[self.module.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(
            response,
            "courses/manage/module/content_list.html",
        )
        self.assertEqual(response.context["module"], self.module)

    def test_get_request_unauthorized(self) -> None:
        """
        Тестирование GET запроса без авторизации.
        """
        url = reverse("courses:module_content_list", args=[self.module.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(
            response,
            f"{reverse('accounts:login')}?next={url}",
        )

    def test_get_request_not_owner(self) -> None:
        """
        Тестирование GET запроса с пользователем,
        не являющимся владельцем курса.
        """
        other_user = User.objects.create_user(
            username="other_user",
            password="password123",
        )
        self.client.force_login(other_user)
        url = reverse("courses:module_content_list", args=[self.module.pk])
        response = self.client.get(url)

        self.assertEqual(response.status_code, HTTPStatus.FORBIDDEN)


class TestModuleOrderView(BaseSetUpData, TestCase):
    module1: c_models.Module
    module2: c_models.Module

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.module1 = c_models.Module.objects.create(
            course=cls.course,
            title="Module 1",
            description="Description 1",
            order=1,
        )
        cls.module2 = c_models.Module.objects.create(
            course=cls.course,
            title="Module 2",
            description="Description 2",
            order=2,
        )

    def test_post_valid(self) -> None:
        """Тестирование POST запроса к ModuleOrderView с валидными данными."""
        url = reverse("courses:module_order")

        self.client.force_login(self.owner)
        response = self.client.post(
            url,
            {
                str(self.module1.pk): 2,
                str(self.module2.pk): 1,
            },
            content_type="application/json",
        )
        self.module1.refresh_from_db()
        self.module2.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.module1.order, 2)
        self.assertEqual(self.module2.order, 1)

    def test_post_invalid(self) -> None:
        """Тестирование POST запроса к ModuleOrderView
        с невалидными данными."""
        url = reverse("courses:module_order")

        self.client.force_login(self.owner)
        response = self.client.post(
            url,
            {
                str(self.module1.pk): 2,
                str(self.module2.pk): 1,
                "invalid": 3,
            },
            content_type="application/json",
        )
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

        self.module1.refresh_from_db()
        self.module2.refresh_from_db()
        self.assertNotEqual(self.module1.order, 2)
        self.assertNotEqual(self.module2.order, 1)


class TestContentOrderView(TestCase):
    owner_data: dict[str, str]
    owner: User
    subject_data: dict[str, str]
    subject: c_models.Subject
    course_data: dict[str, Any]
    course: c_models.Course
    module_data: dict[str, Any]
    module: c_models.Module
    text_data: dict[str, Any]
    text_model: c_models.Text
    text_content_type: ContentType
    content1: c_models.Content
    content2: c_models.Content

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "user",
            "email": "user@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.subject_data = {
            "title": "Python Programming",
            "slug": "python-programming",
        }
        cls.subject = c_models.Subject.objects.create(
            **cls.subject_data,
        )

        cls.course_data = {
            "owner": cls.owner,
            "subject": cls.subject,
            "title": "Python",
            "slug": "python",
            "overview": "A comprehensive Python course.",
        }
        cls.course = c_models.Course.objects.create(
            **cls.course_data,
        )

        cls.module_data = {
            "course": cls.course,
            "title": "Math",
            "description": "desc",
        }
        cls.module = c_models.Module.objects.create(
            **cls.module_data,
        )

        cls.text_data = {
            "owner": cls.owner,
            "title": "Test Text",
            "content": "Some content",
        }
        cls.text_model = c_models.Text.objects.create(
            **cls.text_data,
        )
        cls.text_content_type = ContentType.objects.get_for_model(
            c_models.Text,
        )

        cls.content1 = c_models.Content.objects.create(
            module=cls.module,
            content_type=cls.text_content_type,
            object_id=cls.text_model.pk,
        )
        cls.content2 = c_models.Content.objects.create(
            module=cls.module,
            content_type=cls.text_content_type,
            object_id=cls.text_model.pk,
        )

    def test_post_valid(self) -> None:
        """Тестирование POST запроса к ContentOrderView с валидными данными."""
        url = reverse("courses:content_order")

        self.client.force_login(self.owner)
        response = self.client.post(
            url,
            {
                str(self.content1.pk): 2,
                str(self.content2.pk): 1,
            },
            content_type="application/json",
        )
        self.content1.refresh_from_db()
        self.content2.refresh_from_db()
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.content1.order, 2)
        self.assertEqual(self.content2.order, 1)
