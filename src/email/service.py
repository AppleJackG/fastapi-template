import smtplib
from .templates import get_email_registration_confirmation_template
from ..config import settings


class EmailService:

    @staticmethod
    def send_registration_confirmation_email(username: str, recipient_email: str):
        message = get_email_registration_confirmation_template(username, recipient_email)
        with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(message['From'], message['To'], message.as_string())


email_service = EmailService()

