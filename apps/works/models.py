from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default='bi-image', verbose_name='Иконка Bootstrap')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Тег')
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Work(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='works', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    image = models.ImageField(upload_to='works/', blank=True, null=True, verbose_name='Изображение')
    image_url = models.URLField(blank=True, verbose_name='URL изображения')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='works', verbose_name='Категория')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='Теги')
    year = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name='Год')
    is_featured = models.BooleanField(default=False, verbose_name='Рекомендуемая')
    is_published = models.BooleanField(default=True, verbose_name='Опубликована')
    likes_count = models.PositiveIntegerField(default=0, verbose_name='Лайки')
    views_count = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    comments_count = models.PositiveIntegerField(default=0, verbose_name='Комментарии')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'
        ordering = ['-created_at']

    def get_image(self):
        if self.image:
            return self.image.url
        return self.image_url or ''

    def __str__(self):
        return self.title


class Album(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='albums', verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    cover = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='cover_albums', verbose_name='Обложка')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Альбом'
        verbose_name_plural = 'Альбомы'

    def __str__(self):
        return self.title


class AlbumWork(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='album_works')
    work = models.ForeignKey(Work, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('album', 'work')


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'work')
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=True, verbose_name='Одобрен')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['created_at']

    def __str__(self):
        return f'{self.user.username}: {self.text[:50]}'
