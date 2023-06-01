from django.urls import path

from catalog.views import (
    CatalogHome,
    CatalogParsing,
    ProductListView,
    ProductDetailView,
)

app_name = 'catalog'

urlpatterns = [
    path('', CatalogHome.as_view(), name="home"), # noqa
    path('parsing/', CatalogParsing.as_view(), name="parsing"), # noqa
    path('<slug:category_slug>/', ProductListView.as_view(), name='list'), # noqa
    path('<slug:category_slug>/<slug:slug>/', ProductDetailView.as_view(), name='detail'), # noqa
]
