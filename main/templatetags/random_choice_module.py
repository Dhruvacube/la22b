from django import template

register = template.Library()

@register.filter(name='random_choice')
def random_choice(list1):
    from random import choice
    return choice(list1)