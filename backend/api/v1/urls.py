from django.urls import include, path
from rest_framework.routers import DefaultRouter

from backend.apps.courses.api.views import (
    CourseViewSet,
    SubjectListView,
)

router = DefaultRouter()
router.register(r"subjects", SubjectListView, basename="subjects")
router.register(r"courses", CourseViewSet, basename="courses")


urlpatterns = [
    path("v1/", include(router.urls)),
]
