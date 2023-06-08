from django.urls import path

from rest.catalog.views import ProductList, ProductDetail

# from rest_framework import routers
# router = routers.SimpleRouter()
# router.register(r'catalog', ProductList)
# urlpatterns = router.urls

urlpatterns = [
    path('products/', ProductList.as_view()),
    path('products/<uuid:pk>', ProductDetail.as_view())
]
