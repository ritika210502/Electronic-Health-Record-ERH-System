from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_appointment_email(subject, message, recipient):
    send_mail(subject, message, 'ritikachourasia21@gmail.com', [recipient])
