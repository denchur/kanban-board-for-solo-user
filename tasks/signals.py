from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail, EmailMessage
from .models import Task
from django.conf import settings
import os

@receiver(post_save, sender=Task)
def notify_user(sender, instance, *args, **kwargs):
    count = (
        Task.objects.filter(worker = instance.worker, stage=1).count() +
        Task.objects.filter(worker = instance.worker, stage=2).count() +
        Task.objects.filter(worker = instance.worker, stage=3).count()
    )
    
    if count  in [10,15,20,30]:
        subject = 'Несколько незавершенных задач'
        message = f'У вас есть {count} задач, которые ждут выполнения. Пожалуйста, начните их как можно скорее!'
        recipient_list = [instance.worker.email,]
        email_from = settings.EMAIL_HOST_USER
        send_mail(subject,message,email_from,recipient_list,fail_silently=True)