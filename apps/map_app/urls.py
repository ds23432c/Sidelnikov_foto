from django.urls import path
from . import views

urlpatterns = [
    path('', views.map_view, name='map'),
    path('api/creators/', views.creators_json, name='creators_json'),
]
