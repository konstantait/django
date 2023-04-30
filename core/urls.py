from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('catalog/', include('catalog.urls', namespace='catalog')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('exchange/', include('exchange.urls', namespace='exchange')),
    path('', include('home.urls', namespace='home')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
