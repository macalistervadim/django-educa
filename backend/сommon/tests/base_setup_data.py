from typing import Any

from django.contrib.auth.models import User
from django.test import TestCase

import backend.apps.courses.models as c_models


class BaseSetUpData(TestCase):  # TODO: унаследовать от этого класса!!!!!
    """
    Базовый класс setUpData для моделей Course, Module
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
            "username": "user",
            "email": "user@mail.ru",
            "password": "testpassword",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.subject_data = {
            "title": "Python Programming",
            "slug": "python-programming",
        }
        cls.subject = c_models.Subject.objects.create(**cls.subject_data)

        cls.course_data = {
            "owner": cls.owner,
            "subject": cls.subject,
            "title": "Python",
            "slug": "python",
            "overview": "A comprehensive Python course.",
        }
        cls.course = c_models.Course.objects.create(**cls.course_data)
