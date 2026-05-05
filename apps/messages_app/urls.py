from django.urls import path
from . import views

urlpatterns = [
    path('', views.dialog_list, name='dialog_list'),
    path('<int:dialog_id>/', views.dialog_detail, name='dialog_detail'),
    path('start/<str:username>/', views.start_dialog, name='start_dialog'),
    path('<int:dialog_id>/send/', views.send_message, name='send_message'),
    path('api/unread/', views.unread_count_api, name='unread_count_api'),
]
