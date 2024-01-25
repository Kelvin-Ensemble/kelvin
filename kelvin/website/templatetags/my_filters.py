from django import template
register = template.Library()

@register.filter()
def is_numeric(value):
    value = str(value)
    return value.isnumeric()