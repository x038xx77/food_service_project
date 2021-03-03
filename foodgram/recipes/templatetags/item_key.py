from recipes.models import Diet, Purchases
from django.shortcuts import get_object_or_404
from django.template.defaulttags import register
from django import template

register = template.Library() # noqa


@register.simple_tag
def relative_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = []
        for item in querystring:
            if item.split('=')[0] != field_name:
                filtered_querystring.append(item)
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)
    return url


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
    check = user.follower.filter(author=author_id).exists()
    return check


@register.filter
def check_favorite(recipe_id, user):
    check = user.favorites.filter(following_recipe=recipe_id).exists()
    return check


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
