from django.urls import path

from src.apps.courses.views import (
    content_create_update,
    manage_course,
    module_content_list,
)

app_name = "courses"


urlpatterns = [
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
    path(
        "module/<int:module_id>/content/<model_name>/create/",
        content_create_update.ContentCreateUpdateView.as_view(),
        name="module_content_create",
    ),
    path(
        "module/<int:module_id>/content/<model_name>/<pk>/",
        content_create_update.ContentCreateUpdateView.as_view(),
        name="module_content_update",
    ),
    path(
        "content/<int:pk>/delete/",
        content_create_update.ContentDeleteView.as_view(),
        name="module_content_delete",
    ),
    path(
        "module/<int:module_id>/",
        module_content_list.ModuleContentListView.as_view(),
        name="module_content_list",
    ),
]
