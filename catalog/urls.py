from django.urls import path

from .views import ProductListView, ReviewView

app_name = 'catalog'

urlpatterns = [
    path('products/', ProductListView.as_view(), name="products"),
    path('reviews/', ReviewView.as_view(), name="reviews"),
]
