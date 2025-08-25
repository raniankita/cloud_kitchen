# users/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_welcome_email(user_email, username):
    subject = "Welcome Mail!"
    message = f"Hi user,\n\nThank you for registering."
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
    print("Email sent")
    return "Email sent"
