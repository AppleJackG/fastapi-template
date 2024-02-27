from celery import Celery

from ..config import settings
from ..email.service import email_service


celery = Celery(__name__, broker=settings.CELERY_BROKER_URL)


@celery.task
def send_registration_confirmation_email(username: str, recipient_email: str):
    email_service.send_registration_confirmation_email(username, recipient_email)


@celery.task
def add(x, y):
    return x + y