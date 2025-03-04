from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from backend.apps.courses.api.views import CourseViewSet, SubjectListView


class TestUrls(APITestCase):
    def test_subject_list_url(self) -> None:
        url = reverse("subjects-list")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "subjects-list")
        self.assertTrue(issubclass(resolver.func.__class__, SubjectListView))

    def test_course_list_url(self) -> None:
        url = reverse("courses-list")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "courses-list")
        self.assertTrue(issubclass(resolver.func.__class__, CourseViewSet))

    def test_course_enroll_url(self) -> None:
        course_id = 1
        url = reverse("course-enroll", args=[course_id])
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "course-enroll")
        self.assertTrue(issubclass(resolver.func.__class__, CourseViewSet))

    def test_course_contents_url(self) -> None:
        course_id = 1
        url = reverse("course-contents", args=[course_id])
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "course-contents")
        self.assertTrue(issubclass(resolver.func.__class__, CourseViewSet))
