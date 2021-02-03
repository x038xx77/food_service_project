from django.template.defaulttags import register
from django import template


register = template.Library() # noqa


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    if key:
        return dict_data.get(key)


@register.simple_tag
def query_transform(request, **kwargs):
    updated = request.GET.copy()
    for k, v in kwargs.items():
        if v is not None:
            updated[k] = v
        else:
            updated.pop(k, 0)
    return updated.urlencode()
