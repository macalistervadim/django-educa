from django.urls import resolve, reverse
from rest_framework.test import APITestCase

from backend.apps.courses.api.views import CourseViewSet, SubjectListView


class TestUrls(APITestCase):
    def test_subject_list_url(self) -> None:
        url = reverse("subjects-list")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "subjects-list")
        self.assertEqual(resolver.func.cls, SubjectListView)  # type: ignore


    def test_course_list_url(self) -> None:
        url = reverse("courses-list")
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "courses-list")
        self.assertEqual(resolver.func.cls, CourseViewSet)  # type: ignore

    def test_course_enroll_url(self) -> None:
        course_id = 1
        url = reverse("courses-enroll", args=[course_id])
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "courses-enroll")
        self.assertEqual(resolver.func.cls, CourseViewSet)  # type: ignore

    def test_course_contents_url(self) -> None:
        course_id = 1
        url = reverse("courses-contents", args=[course_id])
        resolver = resolve(url)
        self.assertEqual(resolver.view_name, "courses-contents")
        self.assertEqual(resolver.func.cls, CourseViewSet) # type: ignore
