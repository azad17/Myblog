from django.db.models.expressions import F
from celery import shared_task
from django.core.mail import send_mail

'''using celery and redis'''
@shared_task
def send_mail_task(subject,content,sender,receiver):
    send_mail(subject,content,sender,[receiver],fail_silently=False)
    return None