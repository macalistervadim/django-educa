from typing import Any

from django.contrib.auth.models import User
from django.forms import BaseInlineFormSet
from django.test import TestCase

import src.apps.courses.forms as c_forms
import src.apps.courses.models as c_models


class ModuleFormSetTest(TestCase):
    module: c_models.Module
    course: c_models.Course
    owner: User
    subject: c_models.Subject
    formset: type[BaseInlineFormSet]
    course_data: dict[str, Any]

    @classmethod
    def setUpTestData(cls) -> None:
        cls.owner = User.objects.create_user(
            username="testuser", password="testpass",
        )
        cls.subject = c_models.Subject.objects.create(title="Python")
        cls.course_data = {
            "owner": cls.owner,
            "subject": cls.subject,
            "title": "Course 1",
            "slug": "course-1",
            "overview": "A brief description.",
        }
        cls.course = c_models.Course.objects.create(**cls.course_data)

    def test_valid_formset(self) -> None:
        """
        Проверяет, что формсет создаёт модули при валидных данных.
        """
        data = {
            "module_set-TOTAL_FORMS": "2",
            "module_set-INITIAL_FORMS": "0",
            "module_set-0-title": "Module 1",
            "module_set-0-description": "Description 1",
            "module_set-1-title": "Module 2",
            "module_set-1-description": "Description 2",
        }
        formset = c_forms.ModuleFormSet(data,
            instance=self.course, prefix="module_set")
        self.assertTrue(formset.is_valid())
        formset.save()
        self.assertEqual(
            c_models.Module.objects.filter(course=self.course).count(),2)

    def test_invalid_formset(self) -> None:
        """
        Проверяет, что формсет невалиден при отсутствии заголовка.
        """
        data = {
            "module_set-TOTAL_FORMS": "2",
            "module_set-INITIAL_FORMS": "0",
            "module_set-0-title": "",
            "module_set-0-description": "Description 1",
            "module_set-1-title": "Module 2",
            "module_set-1-description": "Description 2",
        }
        formset = c_forms.ModuleFormSet(
            data, instance=self.course, prefix="module_set")
        self.assertFalse(formset.is_valid())
        self.assertIn("title", formset.errors[0])

    def test_update_formset(self) -> None:
        """
        Проверяет, что формсет обновляет существующие модули.
        """
        module = c_models.Module.objects.create(
            course=self.course,
            title="Old Title",
            description="Old Description",
        )
        data = {
            "module_set-TOTAL_FORMS": "1",
            "module_set-INITIAL_FORMS": "1",
            "module_set-0-id": str(module.pk),
            "module_set-0-title": "Updated Title",
            "module_set-0-description": "Updated Description",
        }
        formset = c_forms.ModuleFormSet(data, instance=self.course,
            prefix="module_set")
        self.assertTrue(formset.is_valid())
        formset.save()
        module.refresh_from_db()
        self.assertEqual(module.title, "Updated Title")

    def test_delete_formset(self) -> None:
        """
        Проверяет удаление модуля через `can_delete=True`.
        """
        module = c_models.Module.objects.create(
            course=self.course,
            title="To be deleted",
            description="Will be removed",
        )
        data = {
            "module_set-TOTAL_FORMS": "1",
            "module_set-INITIAL_FORMS": "1",
            "module_set-0-id": str(module.pk),
            "module_set-0-title": "To be deleted",
            "module_set-0-description": "Will be removed",
            "module_set-0-DELETE": "on",
        }
        formset = c_forms.ModuleFormSet(data,
            instance=self.course, prefix="module_set")
        self.assertTrue(formset.is_valid())
        formset.save()
        self.assertFalse(c_models.Module.objects.filter(pk=module.pk).exists())

