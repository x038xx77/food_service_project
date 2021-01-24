from django import forms
from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'ingredients',
            'cooking_time',
            'description',
            'diets',
            'image']

        def __init__(self, *args, **kwargs):
            super(RecipeForm, self).__init__(*args, **kwargs)
            for visible in self.visible_fields():
                visible.field.widget.attrs['class'] = 'form-control'

        # widgets = {
        #     'title': forms.TextInput(attrs={'class': 'form-control'}),
        #     'cooking_time': forms.IntegerField(
        #         attrs={'class': 'form-control'}),
        #     'description': forms.TextInput(attrs={'class': 'form-control'}),
        #     'diet': forms.SelectMultiple(attrs={'class': 'form-control'}),
        #     'image': forms.ImageField(attrs={'class': 'form-control'})
        #     }
