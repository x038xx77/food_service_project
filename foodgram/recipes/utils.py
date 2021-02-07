import json # noqa
from .models import Diet, FollowRecipe


def print_list_purchases(list_all_purchases):
    list_name_set = set()
    list_out = {}
    purchases_out = {}
    for i in list_all_purchases:
        list_out[i[
            'nameIngredient']] = str(
                i['nameIngredient']) + "(" + str(i['unitsIngredient'] + ") - ")
        list_name_set.add(i['nameIngredient'])
    for j in list_name_set:
        weight = 0
        for i in list_all_purchases:
            if i['nameIngredient'] == j:
                weight += int(i['valueIngredient'])
        purchases_out[list_out[j]] = weight
    return purchases_out


def tag_create_chenge_template(recipe, recipe_dict):
    list_diet = []
    for i in recipe_dict:
        try:
            if i == "breakfast":
                diet_breakfast = Diet.objects.get(slug=i)
                recipe.diets.add(diet_breakfast)
                list_diet.append(i)
            elif i == "lunch":
                diet_lunch = Diet.objects.get(slug=i)
                recipe.diets.add(diet_lunch)
                list_diet.append(i)
            elif i == "dinner":
                diet_dinner = Diet.objects.get(slug=i)
                recipe.diets.add(diet_dinner)
                list_diet.append(i)
        except KeyError:
            pass
    return list_diet


def follow_id(queryset):
    follow_list = []
    for is_following in queryset:
        id_follow_recipe = FollowRecipe.objects.filter(
            following_recipe_id=is_following.id
            ).exists()
        if id_follow_recipe:
            follow_list.append(is_following.id)
    return follow_list
