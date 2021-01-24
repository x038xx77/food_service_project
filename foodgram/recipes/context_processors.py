from .models import Diet, Purchases, FollowRecipe, Recipe


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
