from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'cooking_time',
            'description',
            'image']

        widgets = {
                  'title': forms.TextInput(
                      attrs={"class": "form__input"}),
                  'cooking_time': forms.TextInput(
                      attrs={'class': 'form__input'}),
                  'description': forms.Textarea(
                      attrs={'class': 'form__textarea', 'rows': 8}),
                   'image': forms.FileInput(                            # noqa
                    attrs={'class': 'form__file-button'})
                    }


class MyForm(forms.Form):
    breakfast = forms.BooleanField(required=False)
    lunch = forms.BooleanField(required=False)
    dinner = forms.BooleanField(required=False)
