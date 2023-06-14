from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.permissions import IsAuthenticated

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
    path('catalog/', include('catalog.urls', namespace='catalog')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Shop API",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[IsAuthenticated],
)

urlpatterns_swagger = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
            name='schema-redoc'),
]

urlpatterns = urlpatterns_swagger + urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # noqa
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # noqa

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('silk/', include('silk.urls', namespace='silk')),
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
