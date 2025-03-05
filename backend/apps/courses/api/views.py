from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from backend.apps.courses.api.permissions import IsEnrolled
from backend.apps.courses.api.serializers import (
    CourseSerializer,
    CourseWithContentsSerializer,
    SubjectSerializer,
)
from backend.apps.courses.models import Course, Subject


class SubjectListView(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.all()
    serializer_class: type[Serializer] = SubjectSerializer


class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all()
    serializer_class: type[Serializer] = CourseSerializer

    @action(
        detail=True,
        methods=["post"],
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated],
    )
    def enroll(
        self,
        request: Request,
        *args: list,
        **kwargs: dict,
    ) -> Response:
        course: Course = self.get_object()
        course.students.add(request.user)
        return Response({"enrolled": True})

    @action(
        detail=True,
        methods=["get"],
        serializer_class=CourseWithContentsSerializer,
        authentication_classes=[BasicAuthentication],
        permission_classes=[IsAuthenticated, IsEnrolled],
    )
    def contents(
        self,
        request: Request,
        *args: list,
        **kwargs: dict,
    ) -> Response:
        return self.retrieve(request, *args, **kwargs)
