from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site

from core.models import Config
from core.settings import EMAIL_SIGNUP_TEMPLATE # noqa
from profiles.services import get_uidb64_from_pk, get_user_token # noqa

from core.celery import app


@app.task
def send_signup_email(request, user):
    settings = Config.load()
    current_site = get_current_site(request)
    site_name = current_site.name
    domain = current_site.domain
    context = {
        'domain': domain,
        'site_name': site_name,
        'uid': get_uidb64_from_pk(user.pk),
        'token': get_user_token(user),
        'protocol': "https" if request.is_secure() else "http",
    }

    subject = f'Registration {site_name}'
    body = loader.render_to_string(EMAIL_SIGNUP_TEMPLATE, context)
    settings = Config.load()
    email_message = EmailMultiAlternatives(
        subject,
        body,
        settings.contact_email,
        [user.email, ]
    )
    print(email_message.__dict__)
    email_message.send()
