from django.urls import path

from src.apps.homepage.views.homepage import HomepageView

app_name = "homepage"

urlpatterns = [
    path("", HomepageView.as_view(), name="homepage"),
]
