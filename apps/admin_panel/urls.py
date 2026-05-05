from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('users/', views.users_list, name='admin_users'),
    path('users/<int:pk>/active/', views.toggle_user_active, name='admin_user_active'),
    path('users/<int:pk>/verified/', views.toggle_user_verified, name='admin_user_verified'),
    path('works/', views.works_moderation, name='admin_works'),
    path('works/<int:pk>/published/', views.toggle_work_published, name='admin_work_published'),
    path('comments/', views.comments_moderation, name='admin_comments'),
    path('comments/<int:pk>/approved/', views.toggle_comment_approved, name='admin_comment_approved'),
]
