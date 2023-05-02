from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

from catalog.views import (
    ProductListView,
    ProductDetailView,
)

app_name = 'catalog'

urlpatterns = [
    path(
        '',
        TemplateView.as_view(template_name='catalog/index.html'),
        name="home"
    ),
    path(
        '<slug:category_slug>/',
        ProductListView.as_view(),
        name='list'
    ),
    path(
        '<slug:category_slug>/<slug:slug>/',
        ProductDetailView.as_view(),
        name='detail'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
