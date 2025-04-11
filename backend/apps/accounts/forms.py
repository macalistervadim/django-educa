from typing import Any

from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string

from .tasks import send_reset_password_email


class CeleryPasswordResetForm(PasswordResetForm):
    def send_mail(
        self,
        subject_template_name: str,
        email_template_name: str,
        context: dict[str, Any],
        from_email: str | None,
        to_email: str,
        html_email_template_name: str | None = None,
    ) -> None:
        subject = str(render_to_string(subject_template_name, context))
        subject = "".join(subject.splitlines())
        body = render_to_string(email_template_name, context)

        if html_email_template_name is not None:
            html_email = render_to_string(html_email_template_name, context)
        else:
            html_email = None

        send_reset_password_email.delay(
            subject=subject,
            message=body,
            from_email=from_email,
            recipient_list=[to_email],
            html_message=html_email,
        )
