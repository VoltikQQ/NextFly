from django import template

register = template.Library()

@register.filter
def calculate_discount(price, discount):
    return price - (price * discount / 100)