from django.urls import path

from apps.courses.views import manage_course, views

app_name = "courses"

urlpatterns = [  # TODO: test + templates
    path("", views.index, name="index"),
    path(
        "mine/",
        manage_course.ManageCourseListView.as_view(),
        name="manage_course_list",
    ),
    path(
        "create/",
        manage_course.CourseCreateView.as_view(),
        name="course_create",
    ),
    path(
        "<pk>/edit/",
        manage_course.CourseUpdateView.as_view(),
        name="course_edit",
    ),
    path(
        "<pk>/delete/",
        manage_course.CourseDeleteView.as_view(),
        name="course_delete",
    ),
    path(
        "<pk>/module/",
        manage_course.CourseModuleUpdateView.as_view(),
        name="course_module_update",
    ),
]
