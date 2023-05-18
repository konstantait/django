from celery import shared_task
from django.core.mail import send_mail

from core.models import Config


@shared_task
def send_contact_message(email, text):
    subject = 'Contact form'
    message = ''.join(email)
    message = f'{message}\n{text}'
    settings = Config.load()
    send_mail(
        subject,
        message,
        settings.contact_email,
        [settings.contact_email, ],
        fail_silently=False
    )
