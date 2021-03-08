from recipes.models import Diet
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
