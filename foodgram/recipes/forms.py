from django import forms
from .models import Diet, Recipe, Ingredient, RecipeIngridient


class RecipeForm(forms.ModelForm):

    # ingredients = forms.ModelMultipleChoiceField(
    #     queryset=Ingredient.objects.all()
    # )
    # amount = {}

    class Meta:
        model = Recipe
        fields = [
            'title',
            'diets',
            'cooking_time',
            'description',
            'image']
        localized_fields = "__all__"

        widgets = {'title': forms.TextInput(attrs={'class': 'form__input'}),
                   'diets': forms.CheckboxSelectMultiple(
                       choices=[Diet.objects.all()]),
                   'cooking_time': forms.TextInput(
                       attrs={'class': 'form__input'}),
                   'description': forms.Textarea(
                       attrs={'class': 'form__textarea', 'rows': 8}),
                   'image': forms.FileInput(
                       attrs={'class': 'form__file-button'})}

        def __init__(self, data, *args, **kwargs):

            if data is not None:
                data = data.copy()

                for tag in ['breakfast', 'lunch', 'dinner']:
                    if tag in data:
                        data.update({'diets': tag})
            super().__init__(data=data, *args, **kwargs)

        def save(self, commit=True):
            recipe_obj = super(RecipeForm, self).save(commit=False)
            recipe_obj.save()
            recipe_obj.tag.set([tag for tag in self.cleaned_data['diets']])
            self.save_m2m()
            
            return recipe_obj
