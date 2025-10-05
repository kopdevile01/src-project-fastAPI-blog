from __future__ import annotations
import smtplib
from email.message import EmailMessage
from app.celery_app import celery
from app.core.settings import settings


@celery.task(name="send_registration_email")
def send_registration_email(to_email: str, username: str) -> None:
    msg = EmailMessage()
    msg["Subject"] = "Registration successful"
    msg["From"] = settings.smtp_from
    msg["To"] = to_email
    msg.set_content(f"Hi, {username}! Your registration was successful.")

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as s:
            if settings.smtp_user and settings.smtp_password:
                s.login(settings.smtp_user, settings.smtp_password)
            s.send_message(msg)
    except Exception as exc:
        print(f"[email task] skipped sending email: {exc}")
