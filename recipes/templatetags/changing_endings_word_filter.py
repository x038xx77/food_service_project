from django.template.defaulttags import register
from django import template

register = template.Library() # noqa


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
