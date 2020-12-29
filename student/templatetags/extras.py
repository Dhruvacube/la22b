from django import template
register = template.Library()

@register.filter(name='get_val')
def get_val(list1, key):
    return list1[key]