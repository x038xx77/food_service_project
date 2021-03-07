
def get_ingredients_from(request):
    nameIng = [request[key] for key in request if 'nameIngredient' in key]
    valueIng = [request[key] for key in request if 'valueIngredient' in key]
    unitsIng = [request[key] for key in request if 'unitsIngredient' in key]
    ingredients = zip(nameIng, valueIng, unitsIng)
    return ingredients


def get_sort_list_tags(request):
    sort_list = []
    if request.GET.getlist('breakfast', None):
        sort_list.append('breakfast')
    if request.GET.getlist('lunch', None):
        sort_list.append('lunch')
    if request.GET.getlist('dinner', None):
        sort_list.append('dinner')
    return sort_list
