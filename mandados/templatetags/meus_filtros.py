from django import template
import re

register = template.Library()

@register.filter
def apenas_numeros(value):
    return re.sub(r'\D', '', value)
