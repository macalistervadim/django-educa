import unittest
from datetime import datetime
from typing import Any, Generic, TypeVar

import django.core.exceptions
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
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


class BaseSetUpData(TestCase):  # TODO: вынести в файл
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
    module_data: dict[str, Any]

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.module_data = {
            "course": cls.course,
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
        self.assertEqual(
            str(self.module),
            f'{self.module.order}. {self.module_data["title"]}',
        )

    def test_repr_module(self) -> None:
        """
        Тест возвращаемого значения __repr__
        """
        expected_repr = (
            f"Module("
            f"course={self.module.course!r}, "
            f"title={self.module.title!r}, "
            f"description={self.module.description!r}, "
            f"order={self.module.order!r})"
        )
        self.assertEqual(repr(self.module), expected_repr)


T = TypeVar("T", bound="c_models.ItemBase")


@unittest.skip(
    "BaseContentTest is an abstract class and should not be run directly.",
)
class BaseContentTest(Generic[T], TestCase):  # TODO: вынести в файл
    """
    Базовый класс для моделей наследованных от ItemBase
    """

    owner: User
    owner_data: dict[str, str]
    model_data: dict[str, Any]
    model_class: type[T]
    additional_field: str | None = None
    additional_value: Any = None
    instance: T

    class Meta:
        abstract = True

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner_data = {
            "username": "user",
            "email": "user@mail.ru",
        }
        cls.owner = User.objects.create_user(**cls.owner_data)

        cls.model_data = {
            "owner": cls.owner,
            "title": "test",
        }

        if cls.additional_field and cls.additional_value:
            cls.model_data[cls.additional_field] = cls.additional_value

        cls.instance = cls.model_class.objects.create(**cls.model_data)

    def test_common_fields(self) -> None:
        """
        Тест основных полей моделей
        """
        self.assertEqual(self.instance.owner, self.owner)
        self.assertEqual(self.instance.title, self.model_data["title"])
        self.assertIsInstance(self.instance.created, datetime)
        self.assertIsInstance(self.instance.updated, datetime)

    def test_additional_field(self) -> None:
        """
        Тест доп. полей - ImageField, FileField...
        """
        if self.additional_field and self.additional_value:
            if isinstance(self.additional_value, SimpleUploadedFile):
                if self.additional_value.name is not None:
                    expected_file_name = self.additional_value.name.split("/")[
                        -1
                    ].split("_")[0]
                else:
                    self.fail(
                        "additional_value.name is None, but expected a string",
                    )

                actual_file_name_attr = getattr(
                    self.instance,
                    self.additional_field,
                ).name
                if actual_file_name_attr is not None:
                    actual_file_name = actual_file_name_attr.split("/")[
                        -1
                    ].split("_")[0]
                else:
                    self.fail(
                        f"{self.additional_field}.name"
                        f" is None, but expected a string",
                    )

                self.assertEqual(actual_file_name, expected_file_name)
            elif isinstance(self.additional_value, str):
                self.assertEqual(
                    getattr(self.instance, self.additional_field),
                    self.additional_value,
                )
            else:
                self.fail(
                    f"Unexpected type for additional_value: {type(
                        self.additional_value).__name__}",
                )

    def test_str_method(self) -> None:
        """
        Тест метода __str__.
        """
        self.assertEqual(str(self.instance), self.model_data["title"])

    def test_repr_method(self) -> None:
        """
        Тест метода __repr__.
        """
        additional_field_value = ""
        if self.additional_field and self.additional_value:
            if isinstance(self.additional_value, SimpleUploadedFile):
                additional_field_value = f", {self.additional_field}={repr(
                    getattr(self.instance, self.additional_field))}"
            else:
                additional_field_value = f", {self.additional_field}={repr(
                    getattr(self.instance, self.additional_field))}"

        correct_repr = (
            f"{self.model_class.__name__}("
            f"owner={repr(self.owner)}, "
            f"title={repr(self.model_data['title'])}, "
            f"created={repr(self.instance.created)}, "
            f"updated={repr(self.instance.updated)}"
            f"{additional_field_value})"
        )
        self.assertEqual(repr(self.instance), correct_repr)


class TestTextModel(BaseContentTest):
    model_class = c_models.Text
    additional_field = "content"
    additional_value = "something"


class TestFileModel(BaseContentTest):
    model_class = c_models.File
    additional_field = "file"
    additional_value = SimpleUploadedFile(
        "dynamic_test_file.txt",
        b"dummy content",
        content_type="text/plain",
    )


class TestImageModel(BaseContentTest):
    model_class = c_models.Image
    additional_field = "file"
    additional_value = SimpleUploadedFile(
        "dynamic_test_image.jpg",
        b"dummy image data",
        content_type="image/jpeg",
    )


class TestVideoModel(BaseContentTest):
    model_class = c_models.Video
    additional_field = "url"
    additional_value = "https://example.com/video"


class TestContentModel(TestCase):
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
    content: c_models.Content

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

        cls.content = c_models.Content.objects.create(
            module=cls.module,
            content_type=cls.text_content_type,
            object_id=cls.text_model.pk,
        )

    def test_creation_content(self) -> None:
        """
        Тест создания модели Content
        """
        self.assertEqual(c_models.Content.objects.count(), 1)
        content = c_models.Content.objects.first()
        if content is not None:
            self.assertEqual(content.module, self.module)
            self.assertEqual(content.content_type, self.text_content_type)
            self.assertEqual(content.object_id, self.text_model.pk)
            self.assertEqual(content.item, self.text_model)

    def test_str_method(self) -> None:
        """
        Тест метода __str__.
        """
        self.assertEqual(
            str(self.content),
            f"{self.text_model.pk} - {self.text_model}",
        )

    def test_repr_method(self) -> None:
        """
        Тест метода __repr__.
        """
        expected_repr = (
            f"Content("
            f"module={self.module!r}, "
            f"content_type={self.text_content_type!r}, "
            f"object_id={self.text_model.pk}, "
            f"item={self.text_model!r}, "
            f"order={self.content.order!r})"
        )
        self.assertEqual(repr(self.content), expected_repr)

    def test_content_type_choices(self) -> None:
        """
        Тест на ограничение выбора content_type.
        """
        invalid_content_type = ContentType.objects.get_for_model(User)
        with self.assertRaises(django.core.exceptions.ValidationError):
            content = c_models.Content(
                module=self.module,
                content_type=invalid_content_type,
                object_id=self.text_model.pk,
            )
            content.full_clean()

    def test_module_relationship(self) -> None:
        """
        Тест на связь с Module.
        """
        self.assertEqual(self.content.module, self.module)
        self.assertIn(self.content, self.module.contents.all())

    def test_generic_foreign_key(self) -> None:
        """
        Тест на связь через GenericForeignKey.
        """
        self.assertEqual(self.content.item, self.text_model)

    def test_delete_module_cascades(self) -> None:
        """
        Тест на каскадное удаление при удалении Module.
        """
        module_id = self.module.pk
        self.module.delete()
        self.assertFalse(
            c_models.Content.objects.filter(module_id=module_id).exists(),
        )

    def test_delete_item_cascades(self) -> None:
        """
        Тест на каскадное удаление при удалении связанного объекта.
        """
        self.text_model.delete()
        self.assertEqual(c_models.Text.objects.count(), 0)
