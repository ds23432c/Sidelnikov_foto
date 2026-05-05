from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = [
        ('creator', 'Создатель'),
        ('client', 'Клиент'),
        ('admin', 'Администратор'),
    ]
    CREATOR_TYPE_CHOICES = [
        ('photographer', 'Фотограф'),
        ('designer', 'Дизайнер'),
        ('illustrator', 'Иллюстратор'),
        ('videographer', 'Видеограф'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='client', verbose_name='Роль')
    creator_type = models.CharField(max_length=20, choices=CREATOR_TYPE_CHOICES, blank=True, null=True, verbose_name='Тип создателя')
    bio = models.TextField(blank=True, verbose_name='О себе')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    avatar_url = models.URLField(blank=True, verbose_name='URL аватара')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    latitude = models.FloatField(null=True, blank=True, verbose_name='Широта')
    longitude = models.FloatField(null=True, blank=True, verbose_name='Долгота')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Специализация')
    instagram = models.CharField(max_length=100, blank=True, verbose_name='Instagram')
    telegram = models.CharField(max_length=100, blank=True, verbose_name='Telegram')
    website = models.URLField(blank=True, verbose_name='Сайт')
    is_verified = models.BooleanField(default=False, verbose_name='Верифицирован')
    followers_count = models.PositiveIntegerField(default=0, verbose_name='Подписчиков')
    works_count = models.PositiveIntegerField(default=0, verbose_name='Работ')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотров')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        elif self.avatar_url:
            return self.avatar_url
        return None

    def get_creator_type_display_ru(self):
        types = {
            'photographer': 'Фотограф',
            'designer': 'Дизайнер',
            'illustrator': 'Иллюстратор',
            'videographer': 'Видеограф',
        }
        return types.get(self.creator_type, '')

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', verbose_name='Подписчик')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers', verbose_name='На кого подписан')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
