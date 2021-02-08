from .models import Purchases


def purchases(self):

    purchases_count = Purchases.objects.count()
    return {'purchases_count': purchases_count}


def is_purchases(self):
    list_id_recipes_purchases = Purchases.objects.values_list(
        'recipe', flat=True)
    list_purchases = [item for item in list_id_recipes_purchases]
    return {'list_purchases': list_purchases}
