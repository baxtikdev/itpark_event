from time import sleep
from django.core.mail import send_mail
from celery import shared_task
from django.conf import settings


@shared_task
def add(x, y):
    return x + y

@shared_task()
def send_feedback_email_task(email, message):
    sleep(10)
    subject = 'Event Email'
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[email])
