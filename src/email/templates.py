from datetime import datetime
from email.message import EmailMessage
from ..config import settings


def get_email_registration_confirmation_template(username: str, recipient_email: str) -> EmailMessage:
    message = EmailMessage()
    message['Subject'] = 'Добро пожаловать на наш сайт!'
    message['From'] = settings.SMTP_USER
    message['To'] = recipient_email
    message.set_content(
        '<div>'
        f'<h1 style="color: red;">Здравствуйте, {username}, для подтверждения регистрации'
        ' перейдите по ссылке 😊</h1>'
        '<p>Спасибо за регистрацию на нашем сайте!</p>'
        f'<p>Отправлено {datetime.now():%d.%m в %H:%M}</p>'
        '</div>',
        subtype='html'
    )
    return message
