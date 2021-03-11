from .models import Diet


def get_ingredients_from_form(request):
    nameIng = [request[key] for key in request if 'nameIngredient' in key]
    valueIng = [request[key] for key in request if 'valueIngredient' in key]
    unitsIng = [request[key] for key in request if 'unitsIngredient' in key]
    ingredients = zip(nameIng, valueIng, unitsIng)
    return ingredients


def get_sort_list_tags(request):
    tags = Diet.objects.all()
    sort_list = []
    for tag in tags:
        if request.GET.getlist(tag.slug):
            sort_list.append(tag.slug)
    return sort_list
