from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test  # noqa

from catalog.models import Product
from reviews.models import Review
from cart.forms import CartAddProductForm
from catalog.tasks import parse_products

from currencies.services import get_currency, get_user_currency


class CatalogHome(TemplateView):
    template_name = 'catalog/index.html'


class CatalogParsing(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        parse_products()
        return super().get_context_data(**kwargs)


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        products = Product.objects.filter(categories__slug=self.kwargs['category_slug']) # noqa
        currency = get_currency(code=get_user_currency(self.request.session))
        for product in products:
            left = currency.symbol_left
            right = currency.symbol_right
            precision = currency.decimal_place
            value = product.price * currency.rate
            product.price_currency = f'{left}{value:0.{precision}f}{right}'
        return products


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        product = Product.objects.filter(slug=self.kwargs['slug'])
        return product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        context['reviews'] = Review.objects.filter(product__id=context['product'].id) # noqa
        return context
