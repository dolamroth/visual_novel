from django.core.mail import send_mail
from django.conf import settings


def send_email(subject, body, to_address):
    send_mail(subject=subject, message=body, from_email=settings.EMAIL_HOST_USER,
              recipient_list=[to_address])
