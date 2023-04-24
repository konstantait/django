from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from catalog.views import ProductListView, ReviewView, ExportCSV, ImportCSV

app_name = 'catalog'

urlpatterns = [
    path('products/', ProductListView.as_view(), name="products"),
    path('reviews/', ReviewView.as_view(), name="reviews"),
    path('export/', ExportCSV.as_view(), name='export'),
    path('import/', ImportCSV.as_view(), name='import'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
