from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from rest.catalog.urls import urlpatterns as rest_catalog_urlpatterns

rest_urlpatterns = [
    *rest_catalog_urlpatterns,
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('contacts/', include('contacts.urls', namespace='contacts')),
    path('currencies/', include('currencies.urls', namespace='currencies')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('tools/', include('tools.urls', namespace='exchange')),
    path('api/v1/', include(rest_urlpatterns)),
    path('', include('catalog.urls', namespace='catalog')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # noqa
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('silk/', include('silk.urls', namespace='silk')),
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
