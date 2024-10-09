from django import template
from django.db.models import Count

import shop.views as views
from shop.models import Category

register = template.Library()


@register.inclusion_tag('shop/list_categories.html')
def show_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('items')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}

@register.filter
def calculate_discount(price, discount):
    return price - (price * discount / 100)

@register.filter
def times(number):
    return range(number)
