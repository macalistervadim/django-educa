from http import HTTPStatus

from braces.views import CsrfExemptMixin, JsonRequestResponseMixin
from django.http import HttpRequest, JsonResponse
from django.views import View

from backend.apps.courses.models import Content, Module


class ModuleOrderView(
    CsrfExemptMixin,
    JsonRequestResponseMixin,
    View,
):
    def post(self, request: HttpRequest) -> JsonResponse:
        if self.request_json:
            for pk, order in self.request_json.items():
                if not pk.isdigit() or not isinstance(order, int):
                    return JsonResponse(
                        {"error": "Invalid data format"},
                        status=HTTPStatus.BAD_REQUEST,
                    )

            for pk, order in self.request_json.items():
                Module.objects.filter(
                    id=pk,
                    course__owner=request.user
                    if request.user.is_authenticated
                    else None,
                ).update(order=order)

        return self.render_json_response({"saved": "OK"})


class ContentOrderView(
    CsrfExemptMixin,
    JsonRequestResponseMixin,
    View,
):
    def post(self, request: HttpRequest) -> JsonResponse:
        if self.request_json:
            for pk, order in self.request_json.items():
                if not pk.isdigit() or not isinstance(order, int):
                    return JsonResponse(
                        {"error": "Invalid data format"},
                        status=HTTPStatus.BAD_REQUEST,
                    )

            for pk, order in self.request_json.items():
                Content.objects.filter(
                    id=pk,
                    module__course__owner=request.user
                    if request.user.is_authenticated
                    else None,
                ).update(order=order)

        return self.render_json_response({"saved": "OK"})
