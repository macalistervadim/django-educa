from django.urls import path

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
        name="student_registration",  # TODO: test
    ),
    path(
        "enroll-course/",
        student_enroll_course.StudentEnrollCourseView.as_view(),
        name="student_enroll_course",  # TODO: test
    ),
    path(
        "courses/",
        student_course_view.StudentCourseListView.as_view(),
        name="student_course_list",  # TODO: test
    ),
    path(
        "course/<pk>/",
        student_course_view.StudentCourseDetailView.as_view(),
        name="student_course_detail",  # TODO: test
    ),
    path(
        "course/<pk>/<module_id>/",
        student_course_view.StudentCourseDetailView.as_view(),
        name="student_course_detail_module",  # TODO: test
    ),
]
