from recipes.models import Purchases
from django.template.defaulttags import register
from django import template

register = template.Library() # noqa


@register.filter
def check_subscription(author_id, user):
    return user.follower.filter(author=author_id).exists()


@register.filter
def check_favorite(recipe_id, user):
    return user.favorites.filter(following_recipe=recipe_id).exists()


@register.filter
def check_purchase(request, recipe):
    if request.user.is_authenticated:
        return Purchases.objects.filter(user=request.user, recipe=recipe)
    else:
        try:
            return str(recipe.id) in request.session['purchase']
        except KeyError:
            return False


@register.filter
def purchases_count(request):
    if request.user.is_authenticated:
        return Purchases.objects.filter(user=request.user).count()
    else:
        try:
            return len(request.session['purchase'])
        except KeyError:
            return 0
