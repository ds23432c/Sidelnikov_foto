from django.contrib import admin
from .models import Category, Tag, Work, Album, AlbumWork, Like, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'is_published', 'is_featured', 'likes_count', 'views_count')
    list_filter = ('is_published', 'is_featured', 'category')
    list_editable = ('is_published', 'is_featured')
    search_fields = ('title', 'creator__username')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'work', 'text', 'is_approved', 'created_at')
    list_editable = ('is_approved',)


admin.site.register(Album)
admin.site.register(AlbumWork)
admin.site.register(Like)
