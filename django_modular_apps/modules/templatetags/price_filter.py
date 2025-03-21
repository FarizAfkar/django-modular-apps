from django import template
register = template.Library()

@register.filter
def to_rupiah(value):
    return value.replace(',','.')
