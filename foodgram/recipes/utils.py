import json

from .models import Unit

# data_1 = {'рис': '2', 'Яйцо': '3', 'Молоко': '3'}


# def get_unit(data):
#     dimension = []
#     for i in data:
#         print(i)
#         try:
#             unit_dimension = Unit.objects.filter(
#                 ingredients_unit__icontains=i)
#             dimension_1 = unit_dimension[0].dimension
#             if dimension_1 is not None:
#                 dimension.append(dimension_1)
#         except IndexError:
#             pass
#         if dimension[0] is not None:
#             dimension = dimension[0]
#         else:
#             dimension = "шт"
# #     return dimension


# print(get_unit(data_1))


def add_out(data):
    if "image" not in data:
        data["image"] = "test"
    elif "breakfast" not in data:
        data["breakfast"] = "test"
    elif "dinner" not in data:
        data["dinner"] = "test"
    elif "lunch" not in data:
        data["lunch"] = "test"
    return data


def list_ingredients(data):
    del data["csrfmiddlewaretoken"]
    del data["title"]
    del data["cooking_time"]
    del data["description"]
    del data["image"]
    del data["breakfast"]
    del data["dinner"]
    del data["lunch"]
    return data


def ingredient_arrey(request):
    arrey_ingredient = list_ingredients(add_out(request))
    new_list_key_ingridient = []
    j = 1
    for i in range(int(len(arrey_ingredient) / 3)):
        new_list_key_ingridient.append('nameIngredient_' + str(j))
        new_list_key_ingridient.append('valueIngredient_' + str(j))
        new_list_key_ingridient.append('unitsIngredient_' + str(j))
        j += 1
    t = 0
    new_arrey = {}
    for key, value in arrey_ingredient.items():
        new_arrey[new_list_key_ingridient[t]] = value
        t += 1
    return new_arrey
