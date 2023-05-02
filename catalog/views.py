from django.views.generic import ListView, DetailView

from django.contrib.auth.decorators import login_required, user_passes_test  # noqa
from catalog.models import Product
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/list.html'
    context_object_name = 'products'
    extra_context = {'category': Product.get_main_category}

    def get_queryset(self):
        return Product.objects.filter(categories__slug=self.kwargs['category_slug']) # noqa


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/detail.html'
    context_object_name = 'product'
    extra_context = {'category': Product.get_main_category}

    def get_queryset(self):
        return Product.objects.filter(slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_product_form = CartAddProductForm()
        context['cart_product_form'] = cart_product_form
        return context
