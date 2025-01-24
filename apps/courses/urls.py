from django.urls import path

from apps.courses.views import views

app_name = "courses"

urlpatterns = [
    path("", views.index, name="index"),
]
