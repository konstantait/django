from django.urls import path

from rest.catalog.views import (
    ProductList,
    ProductDetail,
    ProductDelete,
    ProductCreate
)

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/create', ProductCreate.as_view()),
    path('products/<uuid:pk>/detail', ProductDetail.as_view()),
    path('products/<uuid:pk>/delete', ProductDelete.as_view())
]
