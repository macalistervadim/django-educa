import unittest
from datetime import datetime
from typing import Any, Generic, TypeVar

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

import backend.apps.courses.models as c_models

T = TypeVar("T", bound="c_models.ItemBase")


@unittest.skip(
    "BaseContentTest is an abstract class and should not be run directly.",
)
class BaseContentTest(Generic[T], TestCase):
    """
    Базовый класс тестов для моделей наследованных от ItemBase
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
                    f"Unexpected type for additional_value: {
                        type(self.additional_value).__name__
                    }",
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
                additional_field_value = f", {self.additional_field}={
                    repr(getattr(self.instance, self.additional_field))
                }"
            else:
                additional_field_value = f", {self.additional_field}={
                    repr(getattr(self.instance, self.additional_field))
                }"

        correct_repr = (
            f"{self.model_class.__name__}("
            f"owner={repr(self.owner)}, "
            f"title={repr(self.model_data['title'])}, "
            f"created={repr(self.instance.created)}, "
            f"updated={repr(self.instance.updated)}"
            f"{additional_field_value})"
        )
        self.assertEqual(repr(self.instance), correct_repr)
