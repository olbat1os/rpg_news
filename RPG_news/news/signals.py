from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import *


@receiver(post_save, sender=Comment)
def new_comment(instance, created, **kwargs):
    if created:

        send_mail(
            subject=f'Новый комментарий к вашему сообщению!',
            message=f'Здрваствуйте, {instance.message.author}, у Вашего сообщения, {instance.message.title}, '
                    f'есть новый комментарий, от {instance.author}. '
                    f' http://127.0.0.1:8000/comments/{instance.id}\n',
            from_email=None,
            recipient_list=[instance.message.author.email],
        )


@receiver(post_save, sender=Comment)
def accept_response_message(instance, **kwargs):
    status = instance.status
    if status:
        send_mail(
            subject=f'Ваш комментарий принят!',
            message=f'Здравствуйте, {instance.author}!\n'
                    f'Ваш комментарий на сообщение "{instance.message.title}" принят.\n'
                    f'Посмотреть сообщение целиком можно по ссылке:\n'
                    f'http://127.0.0.1:8000/comments/{instance.message.id}',
            from_email=None,
            recipient_list=[instance.author.email]
        )
