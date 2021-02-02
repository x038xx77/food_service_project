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

        # def __init__(self, *args, **kwargs):
        #     super(RecipeForm, self).__init__(*args, **kwargs)
        #     for visible in self.visible_fields():
        #         visible.field.widget.attrs['class'] = 'form-control'

        widgets = {
                  'title': forms.TextInput(
                      attrs={"class": "form__input"}),
                  'cooking_time': forms.TextInput(
                      attrs={'class': 'form__input'}),
                  'description': forms.Textarea(
                      attrs={'class': 'form__textarea', 'rows': 8}),
              }
