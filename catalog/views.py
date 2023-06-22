from django.db.models import OuterRef, Exists
from django.views.generic import TemplateView, DetailView
from django.contrib.auth.decorators import login_required, user_passes_test  # noqa
from django_filters.views import FilterView

from catalog.models import Product
from reviews.models import Review
from cart.forms import CartAddProductForm
from catalog.tasks import parse_products

from catalog.filters import ProductFilter


class CatalogHome(TemplateView):
    template_name = 'catalog/index.html'


class CatalogParsing(TemplateView):
    template_name = 'catalog/index.html'

    def get_context_data(self, **kwargs):
        parse_products()
        return super().get_context_data(**kwargs)


class ProductListView(FilterView):
    model = Product
    template_name = 'catalog/list.html'
    context_object_name = 'products'
    paginate_by = 8
    filterset_class = ProductFilter
    ordering = ['name']

    def get_queryset(self):
        products = Product.objects.filter(categories__slug=self.kwargs['category_slug']) # noqa
        products = products.select_related('currency').all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering,)
            products = products.order_by(*ordering)
        # favorite = Favorite.objects.filter(product=OuterRef('pk'), user=self.request.user) # noqa
        favorite = self.request.user.favorites.filter(id=OuterRef('pk'))
        products = products.annotate(favorite=Exists(favorite))
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
