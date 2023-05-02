import csv

from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views import View
from django.views.generic import FormView

from django.contrib.auth.decorators import login_required, user_passes_test  # noqa
from django.utils.decorators import method_decorator

from core.constants import (
    CSV_FIELDS_DELIMITER,
    CSV_IN_FIELD_DELIMITER,
    IMAGE_PLACEHOLDER,
)

from catalog.models import Product
from tools.forms import UploadCSVForm


class LoadCSV(View):

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


class UploadCSV(FormView):
    form_class = UploadCSVForm
    template_name = 'tools/upload.html'
    success_url = reverse_lazy('catalog:home')

    @method_decorator(login_required)
    @method_decorator(user_passes_test(lambda u: u.is_staff))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
