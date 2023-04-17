from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import FormView, ListView

from .models import Product
from .forms import ReviewForm
from django.urls import reverse, reverse_lazy


class ProductListView(ListView):
    template_name = 'catalog/products.html'
    context_object_name = 'products'
    model = Product


class ReviewView(FormView):
    template_name = 'catalog/reviews.html'
    form_class = ReviewForm

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
