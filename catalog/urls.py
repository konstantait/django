from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from catalog.views import (
    ProductListView,
    ProductDetailView,
)

app_name = 'catalog'

urlpatterns = [
    path(
        '<slug:category_slug>/',
        ProductListView.as_view(),
        name='product_list'
    ),
    path(
        '<slug:category_slug>/<slug:slug>/',
        ProductDetailView.as_view(),
        name='product_detail'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
