from django.urls import path
from django.views.generic import TemplateView

from catalog.views import (
    ProductListView,
    ProductDetailView,
)

app_name = 'catalog'

urlpatterns = [
    path('', TemplateView.as_view(template_name='catalog/index.html'), name="home"), # noqa
    path('<slug:category_slug>/', ProductListView.as_view(), name='list'), # noqa
    path('<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='detail'), # noqa
]
