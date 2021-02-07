import json # noqa
from .models import Diet, FollowRecipe, Ingredient
from django.http import JsonResponse


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


def tag_create_change_template(recipe, recipe_dict):
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


def ingredient_array(request):
    if "image" not in request:
        request["image"] = "value"
    if "breakfast" not in request:
        request["breakfast"] = "value"
    if "dinner" not in request:
        request["dinner"] = "value"
    if "lunch" not in request:
        request["lunch"] = "value"
    del request["csrfmiddlewaretoken"]
    del request["title"]
    del request["cooking_time"]
    del request["description"]
    del request["image"]
    del request["breakfast"]
    del request["dinner"]
    del request["lunch"]
    new_list_key_ingredient = []
    j = 1
    for i in range(int(len(request) / 3)):
        new_list_key_ingredient.append('nameIngredient_' + str(j))
        new_list_key_ingredient.append('valueIngredient_' + str(j))
        new_list_key_ingredient.append('unitsIngredient_' + str(j))
        j += 1
    t = 0
    new_arrey = {}
    for key, value in request.items():
        new_arrey[new_list_key_ingredient[t]] = value
        t += 1
    update = []
    items = list(new_arrey.items())
    for i in range(len(items) // 3):
        _tmp = items[3 * i:3 * (i + 1)]
        update.append(_tmp)
    new_list_key = ["nameIngredient", "valueIngredient", "unitsIngredient"]
    old_arrey = update
    new_arrey_list = []
    for i in old_arrey:
        new_dict = {}
        t = 0
        for key, value in dict(i).items():
            new_dict[new_list_key[t]] = value
            t += 1
        new_arrey_list.append(new_dict)
    return new_arrey_list


def data_conversion_get_unitsIngredient(unit_dimension):
    unit_value = {}
    list_unit_value = []
    forloop_i = 1
    for i in unit_dimension:
        unit_value['title_' + str(forloop_i)] = i.title
        unit_value['dimension_' + str(forloop_i)] = i.dimension
        forloop_i += 1
    update = []
    items = list(unit_value.items())
    for split_parts in range(len(items) // 2):
        _tmp = items[2 * split_parts:2 * (split_parts + 1)]
        update.append(_tmp)
    new_list_key = ["title", "dimension"]
    old_arrey = update
    list_unit_value = []
    for i in old_arrey:
        new_dict = {}
        counter_new_value = 0
        for key, value in dict(i).items():
            new_dict[new_list_key[counter_new_value]] = value
            counter_new_value += 1
        list_unit_value.append(new_dict)
    return list_unit_value
