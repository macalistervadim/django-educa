# Стандарты кодирования

## Python

### Форматирование кода
- Ruff для быстрого линтинга и форматирования
- Mypy для статической типизации
- Line length: 79 символов
- Отступы: 4 пробела
- Кодировка: UTF-8

### Именование
- Классы: `PascalCase`
- Функции и методы: `snake_case`
- Переменные: `snake_case`
- Константы: `UPPER_CASE`
- Приватные атрибуты: `_leading_underscore`

### Импорты
```python
# Стандартная библиотека
import os
from pathlib import Path

# Сторонние зависимости
from rest_framework import viewsets
from django.db import models

# Локальные импорты
from backend.apps.courses.models import Course
```

### Docstrings 
```python
def calculate_grade(score: float) -> str:
    """
    Calculate grade based on score.

    Args:
        score (float): Student's score (0-100)

    Returns:
        str: Letter grade (A, B, C, D, F)

    Raises:
        ValueError: If score is not between 0 and 100
    """
```

## Django
### Models
```python
class Course(models.Model):
    title = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created"]
        indexes = [
            models.Index(fields=["-created"]),
        ]
        
    def __str__(self):
        return self.title
```

### Views
```python
class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(
            owner=self.request.user,
        )
```

### REST API
### URLs
- Используйте существительные во множественном числе
- Версионирование через URL: /api/v1/
- Вложенные ресурсы через /
- Фильтры через query parameters

### Response Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Тестирование
### Unit Tests
```python
class TestCourse(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Python Basic",
        )
    
    def test_course_creation(self):
        self.assertEqual(self.course.title, "Python Basic")
```

### Integration Tests
```python
class TestCourseAPI(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("api:courses-list")
    
    def test_course_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
```

## Git
### Ветки

- production: продакшн-ветка
- development: разработка 
- feature/*: новый функционал
- bugfix/*: исправление ошибок
- release/*: подготовка релиза

### Commits
```
feat(courses): add course rating system
fix(course): handle empty course list
docs(api): update API documentation
test(rating): add tests for rating system
refactor: simplify grade calculation
```

## Безопасность

### Sensitive Data
- Не хранить секреты в коде
- Использовать Vault для секретов
- Проверять код на утечки данных

### Input Validation
- Валидировать все входные данные
- Использовать подготовленные запросы
- Экранировать спецсимволы

## Оптимизация
### Database
- Использовать индексы
- Оптимизировать запросы
- Избегать N+1 проблемы

### Caching
- Кэшировать тяжелые запросы
- Использовать Redis
- Инвалидировать кэш при изменениях

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 