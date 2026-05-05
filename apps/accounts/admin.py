from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'creator_type', 'city', 'is_verified')
    list_filter = ('role', 'creator_type', 'is_verified')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительно', {'fields': ('role', 'creator_type', 'bio', 'avatar', 'avatar_url',
                                       'city', 'latitude', 'longitude', 'specialization',
                                       'instagram', 'telegram', 'website', 'is_verified',
                                       'followers_count', 'works_count', 'views_count')}),
    )

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'following', 'created_at')
