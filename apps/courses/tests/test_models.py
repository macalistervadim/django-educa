from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

import apps.courses.models as c_models


class TestsSubjectModel(TestCase):
    subject: c_models.Subject
    data: dict[str, str]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.data = {
            "title": "Python Programming",
            "slug": "python-programming",
        }
        cls.subject = c_models.Subject.objects.create(**cls.data)

    def test_subject_creation(self) -> None:
        """Тест создания объекта Subject."""
        self.assertEqual(c_models.Subject.objects.count(), 1)
        subject = c_models.Subject.objects.first()
        if subject is not None:
            self.assertEqual(subject.title, self.data["title"])
            self.assertEqual(subject.slug, self.data["slug"])

    def test_str_method(self) -> None:
        """Тест метода __str__."""
        self.assertEqual(str(self.subject), self.data["title"])

    def test_repr_method(self) -> None:
        """Тест метода __repr__."""
        expected_repr = (
            f"Subject(title={self.subject.title!r}, "
            f"slug={self.subject.slug!r})"
        )
        self.assertEqual(repr(self.subject), expected_repr)

    def test_slug_field_unique_constraint(self) -> None:
        """Тест ограничения уникальности поля slug."""
        with self.assertRaises(Exception) as context:
            c_models.Subject.objects.create(
                title="Duplicate Slug Test",
                slug=self.data["slug"],
            )
        self.assertIn(
            "duplicate key value violates unique constraint",
            str(context.exception),
        )

    def test_ordering(self) -> None:
        """Тест сортировки объектов по полю title."""
        c_models.Subject.objects.create(title="A Course", slug="a-course")
        c_models.Subject.objects.create(title="Z Course", slug="z-course")
        subjects = c_models.Subject.objects.all()
        titles = [subject.title for subject in subjects]
        self.assertEqual(
            titles,
            ["A Course", "Python Programming", "Z Course"],
        )


class BaseSetUpData(TestCase):
    """
    Базовый класс setUpData для моделей Course, Module
    """

    owner: User
    subject: c_models.Subject
    course: c_models.Course
    owner_data: dict[str, str]
    subject_data: dict[str, str]
    course_data: dict[str, str]

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
        cls.subject = c_models.Subject.objects.create(**cls.subject_data)

        cls.course_data = {
            "owner": cls.owner,  # type: ignore
            "subject": cls.subject,  # type: ignore
            "title": "Python",
            "slug": "python",
            "overview": "A comprehensive Python course.",
        }
        cls.course = c_models.Course.objects.create(**cls.course_data)


class TestsCourseModel(BaseSetUpData):
    def test_course_creation(self) -> None:
        """Тест создания объекта Course."""
        self.assertEqual(c_models.Course.objects.count(), 1)
        course = c_models.Course.objects.first()
        if course is not None:
            self.assertEqual(course.owner, self.owner)
            self.assertEqual(course.subject, self.subject)
            self.assertEqual(course.title, self.course_data["title"])
            self.assertEqual(course.slug, self.course_data["slug"])
            self.assertEqual(course.overview, self.course_data["overview"])
            self.assertIsInstance(course.created, datetime)

    def test_str_method(self) -> None:
        """Тест метода __str__."""
        self.assertEqual(str(self.course), self.course_data["title"])

    def test_repr_method(self) -> None:
        """Тест метода __repr__."""
        expected_repr = (
            f"Course("
            f"owner={self.owner!r}, "
            f"subject={self.subject!r}, "
            f"title={self.course.title!r}, "
            f"slug={self.course.slug!r}, "
            f"overview={self.course.overview!r}, "
            f"created={self.course.created!r})"
        )
        self.assertEqual(repr(self.course), expected_repr)

    def test_slug_field_unique_constraint(self) -> None:
        """Тест уникальности поля slug."""
        with self.assertRaises(Exception) as context:
            c_models.Course.objects.create(
                owner=self.owner,
                subject=self.subject,
                title="Another Python Course",
                slug=self.course_data["slug"],
                overview="Another overview",
            )
        self.assertIn(
            "duplicate key value violates unique constraint",
            str(context.exception),
        )

    def test_ordering(self) -> None:
        """Тест сортировки объектов по полю created (убывание)."""
        c_models.Course.objects.create(
            owner=self.owner,
            subject=self.subject,
            title="Older Course",
            slug="older-course",
            overview="Older course overview.",
            created="2023-01-01T00:00:00Z",
        )
        courses = c_models.Course.objects.all()
        titles = [course.title for course in courses]
        self.assertEqual(titles, ["Older Course", "Python"])

    def test_cascade_on_owner_deletion(self) -> None:
        """Тест каскадного удаления при удалении владельца."""
        self.owner.delete()
        self.assertEqual(c_models.Course.objects.count(), 0)

    def test_cascade_on_subject_deletion(self) -> None:
        """Тест каскадного удаления при удалении предмета."""
        self.subject.delete()
        self.assertEqual(c_models.Course.objects.count(), 0)

    def test_created_timestamp_on_creation(self) -> None:
        """Тест на корректность временной метки в поле created."""
        course = c_models.Course.objects.create(
            owner=self.owner,
            subject=self.subject,
            title="Test Course with Timestamp",
            slug="test-course-timestamp",
            overview="Test overview",
        )
        self.assertIsInstance(course.created, datetime)
        self.assertTrue(course.created <= timezone.now())


class TestModuleModel(BaseSetUpData):
    module: c_models.Module
    module_data: dict[str, str]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.module_data = {
            "course": cls.course,  # type: ignore
            "title": "Math",
            "description": "desc",
        }
        cls.module = c_models.Module.objects.create(**cls.module_data)

    def test_module_creation(self) -> None:
        """
        Тест создания модуля.
        """
        self.assertEqual(c_models.Module.objects.count(), 1)
        module = c_models.Module.objects.first()
        if module is not None:
            self.assertEqual(module.course, self.module_data["course"])
            self.assertEqual(module.title, self.module_data["title"])
            self.assertEqual(
                module.description,
                self.module_data["description"],
            )

    def test_str_module(self) -> None:
        """
        Тест возвращаемого значения __str__
        """
        self.assertEqual(str(self.module), self.module_data["title"])

    def test_repr_module(self) -> None:
        """
        Тест возвращаемого значения __repr__
        """
        expected_repr = (
            f"Module("
            f"course={self.module.course!r}, "
            f"title={self.module.title!r}, "
            f"description={self.module.description!r})"
        )
        self.assertEqual(repr(self.module), expected_repr)


class BaseContentTestMixin:
    """
    Базовый тестовый класс для тестирования моделей,
    унаследованных от ItemBase.
    """
    owner: User
    owner_data: dict[str, str]
    model_data: dict[str, str]

    model_class = None
    additional_field = None
    additional_value = None

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "user",
            "email": "user@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.model_data = {
            "owner": cls.owner,  # type: ignore
            "title": "test",
        }

        if cls.additional_field and cls.additional_value:
            cls.model_data[cls.additional_field] = cls.additional_value

        cls.instance = cls.model_class.objects.create(**cls.model_data)

    def test_common_fields(self) -> None:
        """
        Тестирование общих полей (owner, title, created, updated).
        """
        self.assertEqual(self.instance.owner, self.owner)
        self.assertEqual(self.instance.title, self.model_data["title"])
        self.assertIsInstance(self.instance.created, datetime)
        self.assertIsInstance(self.instance.updated, datetime)

    def test_additional_field(self) -> None:
        """
        Тестирование специфичного поля.
        """
        if self.additional_field and self.additional_value:
            self.assertEqual(
                getattr(self.instance, self.additional_field),
                self.additional_value,
            )

    def test_str_method(self) -> None:
        """
        Тестирование метода __str__.
        """
        self.assertEqual(str(self.instance), self.model_data["title"])

    def test_repr_method(self) -> None:
        """
        Тестирование метода __repr__.
        """
        additional_field_value = (
            f", {self.additional_field}={self.additional_value!r}"
            if self.additional_field and self.additional_value
            else ""
        )
        correct_repr = (
            f"{self.model_class.__name__}("
            f"owner={self.owner!r}, "
            f"title={self.model_data['title']!r}, "
            f"created={self.instance.created!r}, "
            f"updated={self.instance.updated!r}"
            f"{additional_field_value})"
        )
        self.assertEqual(repr(self.instance), correct_repr)


class TestTextModel(BaseContentTestMixin, TestCase):
    model_class = c_models.Text
    additional_field = "content"
    additional_value = "something"


class TestFileModel(BaseContentTestMixin, TestCase):
    model_class = c_models.File
    additional_field = "file"
    additional_value = "test_file.txt"  # todo вставить заглушку


class TestImageModel(BaseContentTestMixin, TestCase):
    model_class = c_models.Image
    additional_field = "file"
    additional_value = "test_image.jpg"  # todo вставить заглушку


class TestVideoModel(BaseContentTestMixin, TestCase):
    model_class = c_models.Video
    additional_field = "url"
    additional_value = "https://example.com/video"
