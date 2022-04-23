import django.dispatch
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from settings.models import MailTemplates
from .utils import send_email
from django.conf import settings

reset_password_token_created = django.dispatch.Signal(
    providing_args=['instance', 'reset_password_token']
)

pre_password_reset = django.dispatch.Signal(providing_args=['user'])

post_password_reset = django.dispatch.Signal(providing_args=['user'])


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email = reset_password_token.user.email

    tpl = MailTemplates.objects.get(alias='password-reset')

    reset_password_url = '{}/reset/pass/{}'.format(settings.FRONTEND_DOMAIN, reset_password_token.key)
 
    data = [
        {'name': '{username}', 'value': reset_password_token.user.username},
        {'name': '{email}', 'value': email},
        {'name': '{reset_password_url}', 'value': reset_password_url}
    ]

    tpl.parse(data)

    send_email(email, tpl)
