from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, RedirectView, DetailView

from core.decorators import ajax_required
from catalog.models import Product


class List(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'favorites/list.html'
    context_object_name = 'products'
    login_url = reverse_lazy('profiles:login')

    def get_queryset(self):
        if self.request.user.pk:
            return Product.objects.filter(favorites=self.request.user.pk) # noqa
        return Product.objects.none()


class Toggle(LoginRequiredMixin, DetailView):
    model = Product
    login_url = reverse_lazy('profiles:login')

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        if product.favorites.filter(id=self.request.user.pk):
            product.favorites.remove(self.request.user)
        else:
            product.favorites.add(self.request.user)
        product.save()
        return HttpResponseRedirect(reverse_lazy('favorites:list'))


class Clear(LoginRequiredMixin, RedirectView):
    http_method_names = ['post']
    url = reverse_lazy('favorites:list')
    login_url = reverse_lazy('profiles:login')

    def get_redirect_url(self, *args, **kwargs):
        self.request.user.favorites.clear()
        self.request.user.save()
        return super().get_redirect_url(*args, **kwargs)


class AJAXToggle(DetailView):
    model = Product

    @method_decorator(login_required)
    @method_decorator(ajax_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        created = True
        if product.favorites.filter(id=self.request.user.pk):
            product.favorites.remove(self.request.user)
            created = False
        else:
            product.favorites.add(self.request.user)
        product.save()
        return JsonResponse({'favourite': created})
