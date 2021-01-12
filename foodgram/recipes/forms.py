from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['diet', 'title', 'image']
        labels = {
            'diet': ('Рацион'),
        }
        help_texts = {
            'diet': ('Справочный текст поля'),
        }
