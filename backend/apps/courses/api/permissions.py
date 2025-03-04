from typing import Any, Literal

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View


class IsEnrolled(BasePermission):
    def has_object_permission(
        self,
        request: Request,
        view: View,
        obj: Any,
    ) -> Literal[True]:
        if obj.students.filter(id=request.user.id).exists():
            return True
        return False  # type: ignore
