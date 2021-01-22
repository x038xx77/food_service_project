from .models import Purchases


def purchases_count(self):
    purchases_count = Purchases.objects.count()
    return {'purchases_count': purchases_count}


def follow_author(self):
    follow_author = True

# def flag_true(self):
#     return JsonResponse({"success": True})
