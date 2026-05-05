from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')
    role = forms.ChoiceField(choices=[('client', 'Клиент'), ('creator', 'Создатель')], label='Роль')
    creator_type = forms.ChoiceField(
        choices=[('', '— выберите —')] + list(User.CREATOR_TYPE_CHOICES),
        required=False, label='Тип создателя'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'creator_type', 'password1', 'password2')

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get('role')
        creator_type = cleaned.get('creator_type')
        if role == 'creator' and not creator_type:
            self.add_error('creator_type', 'Укажите тип создателя')
        return cleaned


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя или Email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'email', 'bio',
            'avatar', 'avatar_url', 'city', 'latitude', 'longitude',
            'specialization', 'instagram', 'telegram', 'website',
            'creator_type',
        ]
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'bio': 'О себе',
            'avatar': 'Аватар (файл)',
            'avatar_url': 'Аватар (URL)',
            'city': 'Город',
            'latitude': 'Широта',
            'longitude': 'Долгота',
            'specialization': 'Специализация',
            'instagram': 'Instagram',
            'telegram': 'Telegram',
            'website': 'Сайт',
            'creator_type': 'Тип создателя',
        }
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '55.7558'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001', 'placeholder': '37.6173'}),
        }
