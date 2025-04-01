from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

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
    path("forgot-password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/registration/password_reset_form.html",
            success_url=reverse_lazy("accounts:password_reset_done"),
            email_template_name="accounts/registration/password_reset_email.html",
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="accounts/registration/password_reset_confirm.html",
            success_url=reverse_lazy("accounts:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]
