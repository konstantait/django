from decimal import Decimal
from catalog.models import Product

from core.settings import CART_SESSION_ID


class Cart:
    def __init__(self, request):
        self.session = request.session
        if '_auth_user_id' in self.session:
            self.uid = request.session['_auth_user_id']
        else:
            self.uid = None
        items = self.session.get(CART_SESSION_ID)
        if not items:
            items = self.session[CART_SESSION_ID] = {}
        self.items = items

    def __iter__(self):
        product_ids = self.items.keys()
        products = Product.objects.filter(id__in=product_ids)
        items = self.items.copy()
        for product in products:
            items[str(product.id)]['product'] = product
        for item in items.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.items.values())

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.items:
            self.items[product_id] = {'quantity': 0, 'price': str(product.price)} # noqa
        if override_quantity:
            self.items[product_id]['quantity'] = quantity
        else:
            self.items[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True
        self.session.save()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.items:
            del self.items[product_id]
            self.save()

    def clear(self):
        del self.session[CART_SESSION_ID]
        self.save()

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.items.values()) # noqa
