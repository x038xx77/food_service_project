from .models import Diet, FavoritesRecipe
from django.shortcuts import get_object_or_404


def tag_create_change_template(recipe, recipe_dict):
    list_diet = []
    for slug in recipe_dict:
        if slug in ['breakfast', 'lunch', 'dinner']:
            diet = get_object_or_404(Diet, slug=slug)
            recipe.diets.add(diet)
            list_diet.append(slug)
    return list_diet


def follow_id(queryset):
    follow_list = []
    for is_following in queryset:
        id_follow_recipe = FavoritesRecipe.objects.filter(
            following_recipe_id=is_following.id
            ).exists()
        if id_follow_recipe:
            follow_list.append(is_following.id)
    return follow_list


def get_ingredients_from(request):
    nameIng = [request[key] for key in request if 'nameIngredient' in key]
    valueIng = [request[key] for key in request if 'valueIngredient' in key]
    unitsIng = [request[key] for key in request if 'unitsIngredient' in key]
    ingredients = zip(nameIng, valueIng, unitsIng)
    return ingredients


def is_empty_ingredients(ingredient_zip):
    try:
        next(ingredient_zip)
        return False
    except StopIteration:
        return True
