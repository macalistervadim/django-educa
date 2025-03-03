from django.urls import path

from backend.apps.courses.views import (
    content_create_update,
    course_detail,
    course_list,
    manage_course,
    module_content_list,
    order_views,
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
    path(
        "module/order/",
        order_views.ModuleOrderView.as_view(),
        name="module_order",
    ),
    path(
        "content/order/",
        order_views.ContentOrderView.as_view(),
        name="content_order",
    ),
    path(
        "",
        course_list.CourseListView.as_view(),
        name="course_list",
    ),
    path(
        "subject/<slug:subject>/",
        course_list.CourseListView.as_view(),
        name="course_list_subject",
    ),
    path(
        "<slug:slug>/",
        course_detail.CourseDetailView.as_view(),
        name="course_detail",
    ),
]
