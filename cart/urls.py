from django.urls import path
from cart import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='detail'),
    path('add/<uuid:product_id>/', views.cart_add, name='add'),
    path('remove/<uuid:product_id>/', views.cart_remove, name='remove'),
    path('clear/', views.cart_clear, name='clear'),
]
