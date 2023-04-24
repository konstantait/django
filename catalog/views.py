import csv

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView, ListView

from django.contrib.auth.decorators import login_required, user_passes_test  # noqa
from django.utils.decorators import method_decorator

from core.constants import (
    CSV_FIELDS_DELIMITER,
    CSV_IN_FIELD_DELIMITER,
    IMAGE_PLACEHOLDER,
)
from catalog.models import Product
from catalog.forms import ReviewForm, ImportCSVForm


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


class ExportCSV(View):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        headers = {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment; filename="products.csv"'
        }
        response = HttpResponse(headers=headers)
        fields_name = [
            'categories',
            'name',
            'model',
            'sku',
            'description',
            'image',
            'price',
            'attributes',
        ]
        writer = csv.DictWriter(
            response,
            fieldnames=fields_name,
            delimiter=CSV_FIELDS_DELIMITER
        )
        writer.writeheader()
        for product in Product.objects.iterator():
            writer.writerow(
                {
                    'categories': CSV_IN_FIELD_DELIMITER.join(product.get_categories()), # noqa
                    'name': product.name,
                    'model': product.model,
                    'sku': product.sku,
                    'description': product.description,
                    'image': product.image.name if product.image else IMAGE_PLACEHOLDER, # noqa
                    'price': product.price,
                    'attributes': CSV_IN_FIELD_DELIMITER.join(product.get_attributes()), # noqa
                }
            )
        if self:
            return response


class ImportCSV(FormView):
    form_class = ImportCSVForm
    template_name = 'catalog/import.html'
    success_url = reverse_lazy('home:index')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
