from django.contrib import admin

from catalog.models import (
    # Attribute,
    # AttributeGroup,
    Category,
    Product,
)
from core.mixins.admin import BaseAdmin


# @admin.register(Attribute)
# class AttributeAdmin(admin.ModelAdmin):
#     list_display = ('name', 'attribute_group', 'sort_order')
#     ordering = ('attribute_group', 'sort_order')
#
#
# @admin.register(AttributeGroup)
# class AttributeGroupAdmin(admin.ModelAdmin):
#     list_display = ('name', 'sort_order', )
#     ordering = ('name', 'sort_order', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'sort_order', )
    ordering = ('sort_order', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('name', 'slug', 'model', 'sku', 'price', )
    ordering = ('slug', )
    prepopulated_fields = {'slug': ('name', )}
