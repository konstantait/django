from django.contrib import admin

from .models import (
    # Language,
    # CategoryDescription,
    # ProductDescription,
    Category,
    Product,
)
from core.mixins.admin import BaseAdmin


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('name', 'model', 'sku', 'price')


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', )
