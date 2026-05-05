from django.db import models
from django.conf import settings


class ServiceOffer(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='services', verbose_name='Создатель')
    title = models.CharField(max_length=200, verbose_name='Название услуги')
    description = models.TextField(verbose_name='Описание')
    price_from = models.PositiveIntegerField(verbose_name='Цена от (₽)')
    price_to = models.PositiveIntegerField(null=True, blank=True, verbose_name='Цена до (₽)')
    delivery_days = models.PositiveSmallIntegerField(verbose_name='Срок выполнения (дней)')

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

    def __str__(self):
        return f'{self.creator.username}: {self.title}'


class OrderRequest(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новая'),
        ('discussing', 'Обсуждается'),
        ('accepted', 'Принята'),
        ('completed', 'Выполнена'),
        ('rejected', 'Отклонена'),
    ]

    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               related_name='client_orders', verbose_name='Клиент')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='creator_orders', verbose_name='Создатель')
    project_type = models.CharField(max_length=200, verbose_name='Тип проекта')
    budget = models.CharField(max_length=100, blank=True, verbose_name='Бюджет')
    description = models.TextField(verbose_name='Описание проекта')
    contact_email = models.EmailField(verbose_name='Email для связи')
    contact_phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'
        ordering = ['-created_at']

    def get_status_color(self):
        colors = {
            'new': 'warning',
            'discussing': 'info',
            'accepted': 'primary',
            'completed': 'success',
            'rejected': 'danger',
        }
        return colors.get(self.status, 'secondary')

    def __str__(self):
        return f'Заявка от {self.client} к {self.creator}'
