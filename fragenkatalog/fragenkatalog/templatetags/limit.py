from django import template

register = template.Library()

@register.filter(is_safe=False)
def limit(value, arg):
    return min(value, arg)