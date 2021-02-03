from .models import Purchases, Tag


def purchases(self):

    purchases_count = Purchases.objects.count()
    return {'purchases_count': purchases_count}


def is_purchases(self):
    list_id_recipes_purchases = Purchases.objects.values_list(
        'recipe', flat=True)
    list_purchases = []
    for id_purchases in list_id_recipes_purchases:
        list_purchases.append(id_purchases)
    return {'list_purchases': list_purchases}


# def is_diets(self):
#     recipe = get_object_or_404(
# Recipe, pk=recipe_id, author__username=username)
#     is_tag_breakfast = recipe.diets.filter(slug="breakfast")
#     is_tag_lunch = recipe.diets.filter(slug="lunch")
#     is_tag_dinner = recipe.diets.filter(slug="dinner")


def get_tags(self):
    is_breakfast = None
    is_lunch = None
    is_dinner = None
    try:
        tag_breakfast = Tag.objects.filter(demension="1")
        if tag_breakfast:
            is_breakfast = 1
        tag_lunch = Tag.objects.filter(demension="2")
        if tag_lunch:
            is_lunch = 2
        tag_dinner = Tag.objects.filter(demension="3")
        if tag_dinner:
            is_dinner = 3
    except IndexError:
        pass

    url_list = []
    try:
        if is_breakfast == int("1") and is_lunch == None and is_dinner == None: # noqa
            url_list.append("1")
        elif is_lunch==int("2") and is_breakfast==None and is_dinner==None: # noqa
            url_list.append("2")
        elif is_dinner==int("3") and is_breakfast==None and is_lunch==None: # noqa
            url_list.append("3")
        elif is_breakfast==int("1") and is_lunch==int("2") and is_dinner==None: # noqa
            url_list.append("1")
            url_list.append("2")
        elif is_breakfast==int("1") and is_dinner==int("3") and is_lunch==None: # noqa
            url_list.append("1")
            url_list.append("3")
        elif is_lunch==int("2") and is_dinner==int("3") and is_breakfast==None: # noqa
            url_list.append("2")
            url_list.append("3")
        elif is_breakfast==int("1") and is_lunch==int("2") and is_dinner==int("3"): # noqa
            url_list.append("1")
            url_list.append("2")
            url_list.append("3")
        elif is_breakfast == None and is_lunch == None and is_dinner == None:
            print("CP-url_list==", url_list)
    except IndexError:
        pass
    print("CP-url_list==", url_list)
    return {
        "tag_breakfast": is_breakfast,
        "tag_lunch": is_lunch,
        "tag_dinner": is_dinner,
        "url_list": url_list}
