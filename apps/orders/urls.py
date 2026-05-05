from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('create/<str:username>/', views.create_order, name='create_order'),
    path('<int:pk>/status/', views.update_status, name='update_order_status'),
    path('services/create/', views.service_create, name='service_create'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
]
