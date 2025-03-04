from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from backend.apps.courses.models import Course, Subject


class SubjectListViewTests(APITestCase):
    def setUp(self) -> None:
        self.subject1 = Subject.objects.create(title="Math", slug="math")
        self.subject2 = Subject.objects.create(title="Science", slug="science")

    def test_list_subjects(self) -> None:
        url: str = reverse("subject-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Math")
        self.assertEqual(response.data[1]["title"], "Science")


class CourseViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass",
        )
        self.course = Course.objects.create(
            title="Django Course",
            slug="django-course",
        )

    def test_enroll_in_course(self) -> None:
        url: str = reverse("course-enroll", args=[self.course.id])
        self.client.login(username="testuser", password="testpass")
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.course.students.filter(id=self.user.id).exists())
        self.assertEqual(response.data["enrolled"], True)

    def test_enroll_not_authenticated(self) -> None:
        url: str = reverse("course-enroll", args=[self.course.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_contents(self) -> None:
        self.course.students.add(self.user)

        url: str = reverse("course-contents", args=[self.course.id])
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Django Course")

    def test_course_contents_not_enrolled(self) -> None:
        url: str = reverse("course-contents", args=[self.course.id])
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
