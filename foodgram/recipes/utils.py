import json

from .models import Unit

data_1 = {'рис': '2', 'Яйцо': '3', 'Молоко': '3'}


def get_unit(data):
    dimension = []
    for i in data:
        print(i)
        try:
            unit_dimension = Unit.objects.filter(
                ingredients_unit__icontains=i)
            dimension_1 = unit_dimension[0].dimension
            if dimension_1 is not None:
                dimension.append(dimension_1)
        except IndexError:
            pass
        if dimension[0] is not None:
            dimension = dimension[0]
        else:
            dimension = "шт"
    return dimension


print(get_unit(data_1))
