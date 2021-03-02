from .models import Diet, Purchases


def all_tags(self):

    all_tags = Diet.objects.values_list(
        'title', flat=True)
    return {'all_tags': all_tags}


def purchases(self):

    purchases_count = Purchases.objects.count()
    return {'purchases_count': purchases_count}


def is_purchases(self):
    list_id_recipes_purchases = Purchases.objects.values_list(
        'recipe', flat=True)
    list_purchases = [item for item in list_id_recipes_purchases]
    return {'list_purchases': list_purchases}
