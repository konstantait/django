from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from catalog.models import Category, Product


class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name')


class ProductDetailSerializer(serializers.ModelSerializer):
    category_names = CategoryListSerializer(read_only=True, many=True, source='categories') # noqa

    class Meta:
        model = Product
        fields = ('id', 'name', 'sku', 'price', 'image', 'category_names')


class ProductCreateSerializer(serializers.ModelSerializer):
    category_names = serializers.ListSerializer(child=CategoryListSerializer(), required=False) # noqa
    # category_names = CategoryListSerializer(read_only=True, many=True, source='categories')  # noqa

    class Meta:
        model = Product
        fields = ('id', 'name', 'sku', 'price', 'image', 'categories', 'category_names')
        read_only_fields = ('id', 'categories')

    def validate_category_names(self, value):
        return Category.objects.filter(
            name__in=[i['name'] for i in value]
        ).values_list('id', flat=True)

    def validate(self, attrs):
        category_names = attrs.pop('category_names', None)
        if category_names:
            attrs['categories'] = category_names
        return attrs


class ProductDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ()

    def validate(self, attrs):
        if self.instance.order_items.exists():
            raise ValidationError("Cannot delete some instances of model "
                                  "'Product' because they are referenced "
                                  "through protected foreign keys", )
        return attrs



