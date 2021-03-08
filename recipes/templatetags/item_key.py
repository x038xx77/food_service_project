from recipes.models import Diet, Purchases
from django.shortcuts import get_object_or_404
from django.template.defaulttags import register
from django import template

register = template.Library() # noqa


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, None)
    return updated.urlencode()


@register.filter
def get_checkbox_style_tag(arg):
    return get_object_or_404(Diet, id=arg).checkbox_style


@register.filter
def get_list_tag(arg):
    list_tag = []
    for tag in arg:
        list_tag.append(tag.title)
    return list_tag


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


@register.filter
def change_ending_recipe(data):
    if data < 3:
        return 'Перейти к автору'
    remaining = (int(data) - 3) % 10
    index = 2
    if remaining == 1:
        index = 0
    elif 2 <= remaining <= 4:
        index = 1
    cases = ['рецепт', 'рецепта', 'рецептов'][index]
    return 'Ещё {} {}'.format(remaining, cases)
