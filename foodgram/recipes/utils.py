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


def is_empty_tag_or_ingredients(recipe_dict):
    ing = [recipe_dict[key] for key in recipe_dict if 'nameIngredient' in key]
    tag_break = [recipe_dict[key] for key in recipe_dict if 'breakfast' in key]
    tag_lunch = [recipe_dict[key] for key in recipe_dict if 'lunch' in key]
    tag_dinner = [recipe_dict[key] for key in recipe_dict if 'dinner' in key]
    if not tag_dinner and not tag_lunch and not tag_break or not ing:
        return True
