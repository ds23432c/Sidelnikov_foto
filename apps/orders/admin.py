from django.contrib import admin
from .models import ServiceOffer, OrderRequest

@admin.register(ServiceOffer)
class ServiceOfferAdmin(admin.ModelAdmin):
    list_display = ('creator', 'title', 'price_from', 'price_to', 'delivery_days')

@admin.register(OrderRequest)
class OrderRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'creator', 'project_type', 'status', 'created_at')
    list_filter = ('status',)
    list_editable = ('status',)
