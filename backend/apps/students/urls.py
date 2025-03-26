from django.urls import path
from django.views.decorators.cache import cache_page

from backend.apps.students.views import (
    student_course_view,
    student_enroll_course,
    student_registration,
)

app_name = "students"

urlpatterns = [
    path(
        "register/",
        student_registration.StudentRegistrationView.as_view(),
        name="student_registration",
    ),
    path(
        "enroll-course/",
        student_enroll_course.StudentEnrollCourseView.as_view(),
        name="student_enroll_course",
    ),
    path(
        "courses/",
        student_course_view.StudentCourseListView.as_view(),
        name="student_course_list",
    ),
    path(
        "course/<pk>/",
        cache_page(60 * 15)(
            student_course_view.StudentCourseDetailView.as_view(),
        ),
        name="student_course_detail",
    ),
    path(
        "course/<pk>/<module_id>/",
        cache_page(60 * 15)(
            student_course_view.StudentCourseDetailView.as_view(),
        ),
        name="student_course_detail_module",
    ),
]
