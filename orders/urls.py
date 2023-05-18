from django.urls import path

from . import views
from orders.views import PaymentView

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('payment/<uuid:pk>/', PaymentView.as_view(), name='payment'),
]
