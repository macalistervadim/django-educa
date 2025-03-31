from base64 import b64encode

from django.urls import reverse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase

from backend.apps.courses.models import Subject
from backend.сommon.tests.base_setup_data import BaseSetUpData


class SubjectListViewTests(APITestCase):
    def setUp(self) -> None:
        self.subject1 = Subject.objects.create(title="Math", slug="math")
        self.subject2 = Subject.objects.create(title="Science", slug="science")

    def test_list_subjects(self) -> None:
        url: str = reverse("subjects-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["title"], "Math")
        self.assertEqual(response.data[1]["title"], "Science")


class CourseViewSetTests(BaseSetUpData, APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.client = APIClient()

    def test_enroll_in_course(self) -> None:
        url = reverse("courses-enroll", args=[self.course.id])

        credentials = b64encode(b"user:testpassword").decode("utf-8")
        self.client.defaults["HTTP_AUTHORIZATION"] = f"Basic {credentials}"

        response: Response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.course.students.filter(id=self.owner.id).exists())
        self.assertEqual(response.data["enrolled"], True)

    def test_enroll_not_authenticated(self) -> None:
        url: str = reverse("courses-enroll", args=[self.course.id])
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_course_contents_not_enrolled(self) -> None:
        url: str = reverse("courses-contents", args=[self.course.id])
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
