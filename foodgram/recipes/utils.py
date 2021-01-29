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
    if "breakfast" not in data:
        data["breakfast"] = "test"
    if "dinner" not in data:
        data["dinner"] = "test"
    if "lunch" not in data:
        data["lunch"] = "test"
    return data


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
