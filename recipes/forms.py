from django import forms
from .models import Diet, Recipe, Ingredient, RecipeIngridient
from .utils import get_ingredients_from_form
from django.shortcuts import get_object_or_404


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = [
            'title',
            'diets',
            'ingredients',
            'cooking_time',
            'description',
            'image']
        localized_fields = '__all__'

        widgets = {'title': forms.TextInput(attrs={'class': 'form__input'}),
                   'diets': forms.CheckboxSelectMultiple(
                       choices=[Diet.objects.all()]),
                   'cooking_time': forms.TextInput(
                       attrs={'class': 'form__input'}),
                   'description': forms.Textarea(
                       attrs={'class': 'form__textarea', 'rows': 8}),
                   'image': forms.FileInput(
                       attrs={'class': 'form__file-button'})}

    def clean(self):
        is_tags, is_ingredient = False, False
        for key in self.data.keys():
            if 'tags' in key:
                is_tags = True
            if 'nameIngredient' in key:
                is_ingredient = True
        if not is_tags:
            self.add_error('diets', 'Отсутствует рацион, поставьте галочки')
        if not is_ingredient:
            self.add_error('ingredients', 'Необходимо добавить ингредиенты')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.save()
        instance.diets.clear()
        for title in self.data.getlist('tags'):
            diet = get_object_or_404(Diet, title=title)
            instance.diets.add(diet)
        ingredients = get_ingredients_from_form(self.data)
        RecipeIngridient.objects.filter(recipe=instance).delete()
        for title, amount, dimension in ingredients:
            ingredient = get_object_or_404(Ingredient, title=title)
            RecipeIngridient.objects.create(
                ingredient=ingredient, recipe=instance, amount=amount)
        return instance
