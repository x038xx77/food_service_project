
def get_ingredients_from(request):
    nameIng = [request[key] for key in request if 'nameIngredient' in key]
    valueIng = [request[key] for key in request if 'valueIngredient' in key]
    unitsIng = [request[key] for key in request if 'unitsIngredient' in key]
    ingredients = zip(nameIng, valueIng, unitsIng)
    return ingredients
