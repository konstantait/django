from django.contrib import admin

from catalog.models import (
    Attribute,
    AttributeGroup,
    Category,
    Product,
    Review
)
from core.mixins.admin import BaseAdmin


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'attribute_group', 'sort_order')
    ordering = ('attribute_group', 'sort_order')


@admin.register(AttributeGroup)
class AttributeGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order')
    ordering = ('sort_order', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort_order', 'date_added', 'date_modified')
    ordering = ('sort_order', 'name')


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('name', 'model', 'sku', 'price',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'text')
