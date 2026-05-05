from django import forms
from .models import OrderRequest, ServiceOffer


class OrderRequestForm(forms.ModelForm):
    class Meta:
        model = OrderRequest
        fields = ['project_type', 'budget', 'description', 'contact_email', 'contact_phone']
        labels = {
            'project_type': 'Тип проекта',
            'budget': 'Бюджет',
            'description': 'Описание проекта',
            'contact_email': 'Email для связи',
            'contact_phone': 'Телефон (необязательно)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
        }


class ServiceOfferForm(forms.ModelForm):
    class Meta:
        model = ServiceOffer
        fields = ['title', 'description', 'price_from', 'price_to', 'delivery_days']
        labels = {
            'title': 'Название услуги',
            'description': 'Описание',
            'price_from': 'Цена от (₽)',
            'price_to': 'Цена до (₽)',
            'delivery_days': 'Срок (дней)',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
