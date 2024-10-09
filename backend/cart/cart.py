from decimal import Decimal
from django.conf import settings
from shop.models import Item


class Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        product_ids = self.cart.keys()
        items = Item.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for item in items:
            cart[str(item.id)]['item'] = item
            cart[str(item.id)]['discount'] = item.discount

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['discount'] = Decimal(item['discount'])
            new_price = item['price'] - item['price'] * item['discount'] / 100
            item['total_price'] = new_price * item['quantity']
            yield item

    def len(self):
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, item, quantity=1, update_quantity=False):
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {'quantity': 0, 'price': str(item.price)}
        if update_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, item):
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def get_total_price(self):
        return sum(Decimal(i['price']) * i['quantity'] for i in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()