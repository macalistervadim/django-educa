from celery import shared_task
from django.core.mail import send_mail


@shared_task(queue="email")
def send_reset_password_email(
    subject: str,
    message: str,
    from_email: str,
    recipient_list: list[str],
    html_message: str | None = None,
) -> int:
    return send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message,
    )
