from rest_framework import serializers
from catalog.models import Category, Product


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class ProductDetailSerializer(serializers.ModelSerializer):
    category_names = CategoryListSerializer(read_only=True, many=True, source='categories') # noqa

    class Meta:
        model = Product
        fields = ('id', 'name', 'sku', 'price', 'image', 'category_names')
