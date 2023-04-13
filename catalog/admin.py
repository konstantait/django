from django.contrib import admin

from .models import (
    Category,
    Product,
    Review
)
from core.mixins.admin import BaseAdmin


@admin.register(Category)
class CategoryAdmin(BaseAdmin):
    list_display = ('name', )


@admin.register(Product)
class ProductAdmin(BaseAdmin):
    list_display = ('name', 'model', 'sku', 'price')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('author', 'product', 'rating', 'text')
