from django.db import connection, models
from django.test import TestCase

from apps.courses.fields import OrderField


class OrderFieldTests(TestCase):
    """
    Тесты для поля OrderField.
    """

    order: OrderField

    def setUp(self) -> None:
        """
        Создаем временную модель для тестирования.
        """

        class TestModel(models.Model):
            name = models.CharField(max_length=100)
            category = models.CharField(max_length=100, null=True, blank=True)
            order = OrderField(for_fields=["category"])

            class Meta:
                app_label = "courses"

        self.TestModel = TestModel

        # Создаем таблицу в базе данных
        with connection.schema_editor() as schema_editor:
            schema_editor.create_model(self.TestModel)

    def tearDown(self) -> None:
        """
        Удаляем временную модель после завершения тестов.
        """
        with connection.schema_editor() as schema_editor:
            schema_editor.delete_model(self.TestModel)

    def test_pre_save_without_for_fields(self) -> None:
        """
        Проверяет, что поле order корректно работает без указания for_fields.
        """
        obj1 = self.TestModel(name="Object 1")
        obj1.save()
        obj2 = self.TestModel(name="Object 2")
        obj2.save()

        self.assertEqual(obj1.order, 0)
        self.assertEqual(obj2.order, 1)

    def test_pre_save_with_for_fields(self) -> None:
        """
        Проверяет, что поле order корректно работает с указанием for_fields.
        """
        obj1 = self.TestModel(name="Object 1", category="A")
        obj1.save()
        obj2 = self.TestModel(name="Object 2", category="A")
        obj2.save()
        obj3 = self.TestModel(name="Object 3", category="B")
        obj3.save()

        self.assertEqual(obj1.order, 0)
        self.assertEqual(obj2.order, 1)
        self.assertEqual(obj3.order, 0)

    def test_pre_save_with_existing_order(self) -> None:
        """
        Проверяет, что поле order не изменяется, если значение уже задано.
        """
        obj1 = self.TestModel(name="Object 1", order=10)
        obj1.save()

        self.assertEqual(obj1.order, 10)

    def test_pre_save_with_empty_queryset(self) -> None:
        """
        Проверяет, что поле order устанавливается в 0, если queryset пуст.
        """
        obj1 = self.TestModel(name="Object 1")
        obj1.save()

        self.assertEqual(obj1.order, 0)
