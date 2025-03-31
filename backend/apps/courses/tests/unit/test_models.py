from datetime import datetime
from typing import Any

import django.core.exceptions
import django.shortcuts
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

import backend.apps.courses.models as c_models
from backend.сommon.tests.base_content_model_test import BaseContentTest
from backend.сommon.tests.base_setup_data import (
    BaseSetUpData,
    BaseSetUpDataContentClasses,
)


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
            f"{self.module.order}. {self.module_data['title']}",
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


class TestContentModel(BaseSetUpDataContentClasses, TestCase):
    text_content_type: ContentType

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()

        cls.text_content_type = ContentType.objects.get_for_model(
            c_models.Text,
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
            self.assertEqual(content.object_id, self.text_content.pk)
            self.assertEqual(content.item, self.text_content)

    def test_str_method(self) -> None:
        """
        Тест метода __str__.
        """
        self.assertEqual(
            str(self.content),
            f"{self.text_content.pk} - {self.text_content}",
        )

    def test_repr_method(self) -> None:
        """
        Тест метода __repr__.
        """
        expected_repr = (
            f"Content("
            f"module={self.module!r}, "
            f"content_type={self.text_content_type!r}, "
            f"object_id={self.text_content.pk}, "
            f"item={self.text_content!r}, "
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
                object_id=self.text_content.pk,
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
        self.assertEqual(self.content.item, self.text_content)

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
        self.text_content.delete()
        self.assertEqual(c_models.Text.objects.count(), 0)
