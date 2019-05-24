from django import template
from django.utils.safestring import mark_safe
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(needs_autoescape=True)
@stringfilter
def highlight(value, search_term=None, autoescape=True):
    if not search_term:
        return mark_safe(value)
    return mark_safe(value.replace(
        search_term,
        "<span class=\"highlighted text-light bg-primary\">%s</span>" % search_term)
    )