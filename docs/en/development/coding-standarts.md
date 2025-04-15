# Coding Standards

## Python

### Code Formatting
- Ruff for quick linting and formatting
- Mypy for static typing
- Line length: 79 characters
- Indentation: 4 spaces
- Encoding: UTF-8

### Naming Conventions
- Classes: `PascalCase`
- Functions and methods: `snake_case`
- Variables: `snake_case`
- Constants: `UPPER_CASE`
- Private attributes: `_leading_underscore`

### Imports
```python
# Standard library
import os
from pathlib import Path

# Third-party dependencies
from rest_framework import viewsets
from django.db import models

# Local imports
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
- Use plural nouns
- Versioning via URL: /api/v1/
- Nested resources via /
- Filters via query parameters

### Response Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error

## Testing
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
### Branches

- production: production branch
- development: development branch
- feature/*: new features
- bugfix/*: bug fixes
- release/*: release preparation

### Commits
```
feat(courses): add course rating system
fix(course): handle empty course list
docs(api): update API documentation
test(rating): add tests for rating system
refactor: simplify grade calculation
```

## Security

### Sensitive Data
- Do not store secrets in code
- Use Vault for secrets
- Scan code for data leaks

### Input Validation
- Validate all input data
- Use prepared statements
- Escape special characters

## Optimization
### Database
- Use indexes
- Optimize queries
- Avoid N+1 problem

### Caching
- Cache heavy queries
- Use Redis
- Invalidate cache on changes

<hr></hr><div> <sub>Built with ❤️ by Startsev Vadim</sub> </div> 