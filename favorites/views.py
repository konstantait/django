from django.views.generic import ListView

from django.contrib.auth.decorators import login_required, user_passes_test  # noqa

from catalog.models import Product

from django.shortcuts import redirect
from django.views.decorators.http import require_POST


class FavoritesListView(ListView):
    model = Product
    template_name = 'favorites/list.html'
    context_object_name = 'products'

    def get_queryset(self):
        if self.request.user.pk:
            return Product.objects.filter(bookmarked_by=self.request.user.pk) # noqa
        return Product.objects.none()

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


# from django.shortcuts import render, redirect, get_object_or_404
# from django.views.decorators.http import require_POST
# from catalog.models import Product
# from .cart import Cart
# from .forms import CartAddProductForm


@require_POST
def add(request, product_id):
    if request.user:
        try:
            Product.objects.get(bookmarked_by=request.user.pk)  # noqa
        except Product.DoesNotExist:
            Product.bookmarked_by.add(request.user)
    return redirect('favorite:list')


@require_POST
def remove(request, product_id):
    return redirect('favorite:list')


@require_POST
def clear(request):
    return redirect('favorite:list')
