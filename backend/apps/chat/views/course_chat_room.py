from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import render


@login_required
def course_char_room(request: HttpRequest, course_id: int) -> HttpResponse:
    try:
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        course = request.user.courses_joined.get(id=course_id)
    except:  # noqa
        return HttpResponseForbidden()
    return render(request, "chat/room.html", {"course": course})
