from django.contrib.auth import views as auth_views
from django.urls import path

app_name = "users"


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/registration/login.html",
        ),
        name="login",
    ),  # TODO: test this
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="users/registration/logged_out.html",
        ),
        name="logout",
    ),  # TODO: test this
]
