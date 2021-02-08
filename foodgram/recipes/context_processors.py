from .models import Purchases


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
