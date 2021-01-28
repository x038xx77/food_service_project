from .models import Diet, Purchases, FollowRecipe, Recipe, Tag


def purchases_count(self):
    purchases_count = Purchases.objects.count()
    return {'purchases_count': purchases_count}


def follow_author(self):
    follow_author = FollowRecipe.objects.all()
    return {'follow_author': follow_author}


def get_diets(self):
    diets = Diet.objects.all()
    diet_breakfast = Diet.objects.get(slug='breakfast')
    diet_lunch = Diet.objects.get(slug='lunch')
    diet_dinner = Diet.objects.get(slug='dinner')
    recipe_breakfast = "Recipe.objects.get(diets=diet_lunch)"
    # recipe_lunch = Recipe.objects.get(slug=diet_lunch)
    # recipe_dinner = Recipe.objects.get(slug=diet_dinner)
    # t = "recipe_breakfast.diets.all()"
    return {
        'diets': diets}


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
        print("===", is_breakfast, is_lunch, is_dinner)
    except IndexError:
        pass

    url_list = []
    if is_breakfast == int("1") and is_lunch == None and is_dinner == None: # noqa
        url_list.append("diet=1")
    elif is_lunch==int("2") and is_breakfast==None and is_dinner==None: # noqa
        url_list.append("diet=2")
    elif is_dinner==int("3") and is_breakfast==None and is_lunch==None: # noqa
        url_list.append("diet=3")
    elif is_breakfast==int("1") and is_lunch==int("2") and is_dinner==None: # noqa
        url_list.append("diet=1 diet=2")
    elif is_breakfast==int("1") and is_dinner==int("3") and is_lunch==None: # noqa
        url_list.append("diet=1 diet=3")
    elif is_lunch==int("2") and is_dinner==int("3") and is_breakfast==None: # noqa
        url_list.append("diet=2 diet=3")
    elif is_breakfast==int("1") and is_lunch==int("2") and is_dinner==int("3"): # noqa
        url_list.append("diet=1 diet=2 diet=3")

    return {
        "tag_breakfast": is_breakfast,
        "tag_lunch": is_lunch,
        "tag_dinner": is_dinner,
        "url_list": url_list}
