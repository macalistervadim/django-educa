from django.urls import path

from backend.apps.students.views import student_registration

app_name = "students"

urlpatterns = [
    path(
        "register/",
        student_registration.StudentRegistrationView.as_view(),
        name="student_registration",
    ),
]
