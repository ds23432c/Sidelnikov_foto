from django.db import models
from django.conf import settings


class Notification(models.Model):
    TYPE_CHOICES = [
        ('like', 'Лайк'),
        ('comment', 'Комментарий'),
        ('follow', 'Подписка'),
        ('order', 'Заявка'),
        ('message', 'Сообщение'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='notifications', verbose_name='Получатель')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='sent_notifications', null=True, blank=True,
                               verbose_name='Отправитель')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name='Тип')
    work = models.ForeignKey('works.Work', on_delete=models.SET_NULL, null=True, blank=True,
                             verbose_name='Работа')
    text = models.TextField(verbose_name='Текст')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']

    def get_icon(self):
        icons = {
            'like': 'bi-heart-fill text-danger',
            'comment': 'bi-chat-fill text-primary',
            'follow': 'bi-person-plus-fill text-success',
            'order': 'bi-envelope-fill text-warning',
            'message': 'bi-chat-dots-fill text-info',
        }
        return icons.get(self.type, 'bi-bell-fill')
