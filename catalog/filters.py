import django_filters

from catalog.models import Product


class ProductFilter(django_filters.FilterSet):

    price = django_filters.RangeFilter()

    class Meta:
        model = Product
        fields = []

    # @property
    # def qs(self):
    #     products = super().qs
    #     return products
