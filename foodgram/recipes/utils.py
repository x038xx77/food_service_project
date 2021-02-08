import json # noqa
from .models import Diet, FollowRecipe


def tag_create_change_template(recipe, recipe_dict):
    list_diet = []
    for slug in recipe_dict:
        try:
            if slug == "breakfast":
                diet_breakfast = Diet.objects.get(slug=slug)
                recipe.diets.add(diet_breakfast)
                list_diet.append(slug)
            elif slug == "lunch":
                diet_lunch = Diet.objects.get(slug=slug)
                recipe.diets.add(diet_lunch)
                list_diet.append(slug)
            elif slug == "dinner":
                diet_dinner = Diet.objects.get(slug=slug)
                recipe.diets.add(diet_dinner)
                list_diet.append(slug)
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


def get_tag(sort_list):
    pass
