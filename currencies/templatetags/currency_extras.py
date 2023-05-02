# import requests
from django import template
from currencies.models import Currency

register = template.Library()


@register.filter
def currency(price, code):
    converting = Currency.objects.get(code=code)
    left = converting.symbol_left
    right = converting.symbol_right
    precision = converting.decimal_place
    value = price * converting.rate
    return f"{left}{value:0.{precision}f}{right}"
