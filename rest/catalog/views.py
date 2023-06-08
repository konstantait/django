from rest_framework import generics
from rest_framework.permissions import AllowAny

from catalog.models import Product
from rest.catalog.serializers import ProductListSerializer, ProductDetailSerializer


class ProductList(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.prefetch_related('categories').all()
    serializer_class = ProductDetailSerializer
    permission_classes = [AllowAny]
