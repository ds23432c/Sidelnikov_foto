from django import forms
from .models import Work, Comment


class WorkForm(forms.ModelForm):
    class Meta:
        model = Work
        fields = ['title', 'description', 'image', 'image_url', 'category', 'tags', 'year', 'is_published']
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'image': 'Изображение (файл)',
            'image_url': 'Изображение (URL)',
            'category': 'Категория',
            'tags': 'Теги',
            'year': 'Год',
            'is_published': 'Опубликовать',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Напишите комментарий...'})}
