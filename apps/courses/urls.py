from django.urls import path

from apps.courses.views import views


urlpatterns = [
    path("", views.index, name="index"),
]
