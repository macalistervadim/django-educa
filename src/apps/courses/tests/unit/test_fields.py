from django.apps import apps
from django.db import connection, models
from django.test import TestCase

from src.apps.courses.fields import OrderField


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True)
    order = OrderField(for_fields=["category"])

    class Meta:
        app_label = "courses"


class OrderFieldTests(TestCase):
    """
    Тесты для OrderField.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Создаем временную модель для тестирования.
        """
        super().setUpClass()

        apps.all_models["courses"]["testmodel"] = TestModel

        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(TestModel)

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Удаляем временную модель после завершения всех тестов.
        """
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(TestModel)

        del apps.all_models["courses"]["testmodel"]

        super().tearDownClass()

    def test_pre_save_without_for_fields(self) -> None:
        """
        Проверяет, что поле order корректно работает без for_fields.
        """
        obj1 = TestModel(name="Object 1")
        obj1.save()
        obj2 = TestModel(name="Object 2")
        obj2.save()

        self.assertIsInstance(obj1.order, int)
        self.assertIsInstance(obj2.order, int)

        self.assertEqual(obj1.order, 0)
        self.assertEqual(obj2.order, 1)

    def test_pre_save_with_for_fields(self) -> None:
        """
        Проверяет работу order при наличии for_fields.
        """
        obj1 = TestModel(name="Object 1", category="A")
        obj1.save()
        obj2 = TestModel(name="Object 2", category="A")
        obj2.save()
        obj3 = TestModel(name="Object 3", category="B")
        obj3.save()

        self.assertIsInstance(obj1.order, int)
        self.assertIsInstance(obj2.order, int)
        self.assertIsInstance(obj3.order, int)

        self.assertEqual(obj1.order, 0)
        self.assertEqual(obj2.order, 1)
        self.assertEqual(obj3.order, 0)

    def test_pre_save_with_existing_order(self) -> None:
        """
        Проверяет, что если order установлен, он не изменяется.
        """
        obj1 = TestModel(name="Object 1", order=10)
        obj1.save()

        self.assertIsInstance(obj1.order, int)

        self.assertEqual(obj1.order, 10)

    def test_pre_save_with_empty_queryset(self) -> None:
        """
        Проверяет, что order = 0, если queryset пуст.
        """
        obj1 = TestModel(name="Object 1")
        obj1.save()

        self.assertIsInstance(obj1.order, int)

        self.assertEqual(obj1.order, 0)
