from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/', views.profile_edit, name='profile_edit'),
    path('cabinet/', views.my_cabinet, name='cabinet'),
    path('u/<str:username>/', views.profile_view, name='profile'),
    path('u/<str:username>/follow/', views.follow_toggle, name='follow_toggle'),
]
