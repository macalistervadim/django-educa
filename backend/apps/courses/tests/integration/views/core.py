from typing import Any

from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType

import backend.apps.courses.models as c_models


class BaseSetUpTestData:
    """
    Базовый класс с созданием данных (owner, subject, course)
    для тестов.
    """

    owner: User
    subject: c_models.Subject
    course: c_models.Course
    owner_data: dict[str, str]
    subject_data: dict[str, str]
    course_data: dict[str, Any]

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


class BaseSetUpDataContentClasses:
    """
    Базовый класс с созданием данных (owner, subject, course, module)
    для тестов.
    """

    subject: c_models.Subject
    user: User
    user_data: dict[str, str]
    course: c_models.Course
    module: c_models.Module
    text_content: c_models.Text
    text_content_data: dict[str, Any]
    content_data: dict[str, Any]
    content: c_models.Content
    item: c_models.ItemBase

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
        cls.text_content = c_models.Text.objects.select_for_update().create(
            owner=cls.user,
            title="test123",
            content="initial content123",
        )

        cls.content = c_models.Content.objects.create(
            module=cls.module,
            content_type=ContentType.objects.get_for_model(c_models.Text),
            object_id=cls.text_content.pk,
            item=cls.text_content,
        )
