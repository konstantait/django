from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views
from orders.views import PaymentView

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/<uuid:pk>/', PaymentView.as_view(), name='payment'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
