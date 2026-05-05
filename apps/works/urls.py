from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('work/<int:pk>/', views.work_detail, name='work_detail'),
    path('work/<int:pk>/like/', views.like_toggle, name='like_toggle'),
    path('work/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('work/create/', views.work_create, name='work_create'),
    path('work/<int:pk>/edit/', views.work_edit, name='work_edit'),
    path('work/<int:pk>/delete/', views.work_delete, name='work_delete'),
]
