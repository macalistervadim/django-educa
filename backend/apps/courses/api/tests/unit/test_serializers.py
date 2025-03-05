from django.contrib.auth.models import User
from django.test import TestCase

from backend.apps.courses.api.serializers import (
    CourseSerializer,
    ModuleSerializer,
    SubjectSerializer,
)
from backend.apps.courses.models import Subject


class TestSubjectSerializer(TestCase):
    def test_valid_serializer(self) -> None:
        data = {
            "title": "Test Title",
            "slug": "test-slug",
        }
        serializer = SubjectSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self) -> None:
        data = {
            "slug": "test-title",
        }
        serializer = SubjectSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestModuleSerializer(TestCase):
    def test_valid_serializer(self) -> None:
        data = {
            "title": "Test Title",
            "description": "Test Description",
        }
        serializer = ModuleSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self) -> None:
        data = {
            "description": "Test Description",
        }
        serializer = ModuleSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class TestCourseSerializer(TestCase):
    owner: User
    subject: Subject

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner = User.objects.create_user(
            username="testuser",
            email="mail@mail.ru",
        )
        cls.subject = Subject.objects.create(
            title="Test Subject",
            slug="test-subject",
        )

    def test_valid_serializer(self) -> None:
        data = {
            "subject": self.subject.id,
            "title": "Test Title",
            "slug": "test-slug",
            "overview": "Test Overview",
            "owner": self.owner.id,
        }
        serializer = CourseSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_serializer(self) -> None:
        data = {
            "title": "Test Title",
            "slug": "test-slug",
            "overview": "Test Overview",
        }
        serializer = CourseSerializer(data=data)
        self.assertFalse(serializer.is_valid())
