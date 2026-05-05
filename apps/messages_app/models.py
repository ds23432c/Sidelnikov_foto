from django.db import models
from django.conf import settings


class Dialog(models.Model):
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='dialogs', verbose_name='Участники')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Диалог'
        verbose_name_plural = 'Диалоги'
        ordering = ['-updated_at']

    def get_other(self, user):
        return self.participants.exclude(pk=user.pk).first()

    def last_message(self):
        return self.messages.order_by('-created_at').first()

    def unread_count(self, user):
        return self.messages.filter(is_read=False).exclude(sender=user).count()


class Message(models.Model):
    dialog = models.ForeignKey(Dialog, on_delete=models.CASCADE, related_name='messages', verbose_name='Диалог')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Отправитель')
    text = models.TextField(blank=True, verbose_name='Текст')
    image = models.ImageField(upload_to='messages/', blank=True, null=True, verbose_name='Фото')
    image_url = models.URLField(blank=True, verbose_name='URL фото')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
        ordering = ['created_at']

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''
