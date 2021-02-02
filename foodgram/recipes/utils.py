import json
from .models import FollowRecipe, Recipe, Tag


def follow_id(queryset):
    follow_list = []
    for is_following in queryset:
        id_follow_recipe = FollowRecipe.objects.filter(
            following_recipe_id=is_following.id
            ).exists()
        if id_follow_recipe:
            follow_list.append(is_following.id)
    return follow_list


def tag_check(request):
    display_type = request.GET.getlist('diet', None)
    print("disp=", display_type)
    if display_type is not None:
        for i in display_type:
            tag = Tag.objects.filter(demension=i)
            if len(tag) == 0:
                Tag.objects.create(demension=i)
            else:
                Tag.objects.filter(demension=i).delete()


def ingredient_arrey(request):
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
    new_list_key_ingridient = []
    j = 1
    for i in range(int(len(request) / 3)):
        new_list_key_ingridient.append('nameIngredient_' + str(j))
        new_list_key_ingridient.append('valueIngredient_' + str(j))
        new_list_key_ingridient.append('unitsIngredient_' + str(j))
        j += 1
    t = 0
    new_arrey = {}
    for key, value in request.items():
        new_arrey[new_list_key_ingridient[t]] = value
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
