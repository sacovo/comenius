from creole import creole2html
from django.utils.safestring import mark_safe
from django import template
register = template.Library()

@register.filter(is_safe=True)
def markup(value):
    return mark_safe(creole2html(value))
