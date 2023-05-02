from django.urls import reverse_lazy
from django.views.generic import ListView, RedirectView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from catalog.models import Product


class List(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'favorites/list.html'
    context_object_name = 'products'
    login_url = reverse_lazy('profiles:login')

    def get_queryset(self):
        if self.request.user.pk:
            return Product.objects.filter(bookmarked_by=self.request.user.pk) # noqa
        return Product.objects.none()


class Add(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('favorites:list')
    login_url = reverse_lazy('profiles:login')

    def get_redirect_url(self, *args, **kwargs):
        # product.get_absolute_url()
        # request.META['HTTP_REFERER']
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        if not product.bookmarked_by.filter(id=self.request.user.pk):
            product.bookmarked_by.add(self.request.user)
        product.save()
        return super().get_redirect_url(*args, **kwargs)


class Remove(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('favorites:list')
    login_url = reverse_lazy('profiles:login')

    def get_redirect_url(self, *args, **kwargs):
        product = get_object_or_404(Product, pk=kwargs['product_id'])
        if product.bookmarked_by.filter(id=self.request.user.pk):
            product.bookmarked_by.remove(self.request.user)
        product.save()
        return super().get_redirect_url(*args, **kwargs)


class Clear(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('favorites:list')
    login_url = reverse_lazy('profiles:login')

    def get_redirect_url(self, *args, **kwargs):
        self.request.user.favorites.clear()
        self.request.user.save()
        return super().get_redirect_url(*args, **kwargs)
