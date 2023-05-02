from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('favorites/', include('favorites.urls', namespace='favorites')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('profiles/', include('profiles.urls', namespace='profiles')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('tools/', include('tools.urls', namespace='exchange')),
    path('', include('catalog.urls', namespace='catalog')),
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
