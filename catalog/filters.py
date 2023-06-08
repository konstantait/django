import django_filters

from catalog.models import Product

from currencies.services import get_currency, get_user_currency


class ProductFilter(django_filters.FilterSet):

    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = []

    @property
    def qs(self):
        products = super().qs
        currency = get_currency(code=get_user_currency(self.request.session))
        for product in products:
            left = currency.symbol_left
            right = currency.symbol_right
            precision = currency.decimal_place
            value = product.price * currency.rate
            product.price_currency = f'{left}{value:0.{precision}f}{right}'
        return products
