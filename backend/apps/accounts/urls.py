from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "accounts"


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/registration/login.html",
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="accounts/registration/logged_out.html",
        ),
        name="logout",
    ),
]
