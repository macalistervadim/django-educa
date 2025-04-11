from django.contrib.auth.views import PasswordResetView

from .forms import CeleryPasswordResetForm


class AsyncPasswordResetView(PasswordResetView):
    form_class = CeleryPasswordResetForm
