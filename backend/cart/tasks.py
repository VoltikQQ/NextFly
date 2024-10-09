from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

from .models import PaymentHistory


@shared_task
def send_payment_confirmation(payment_id):
    payment = PaymentHistory.objects.get(id=payment_id)
    recipient_email = payment.email

    mail_sender = send_mail(
        subject="Here is your product",
        message=f"Thanks for your purchased {payment.user.username}",
        recipient_list=[recipient_email],
        from_email=settings.EMAIL_HOST_USER,
    )

    return mail_sender

# @shared_task
# def bar():
#     return "hello world"
