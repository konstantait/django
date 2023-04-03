from django.contrib import admin

from .models import (
    # Language,
    # CategoryDescription,
    # ProductDescription,
    Category,
    Product,
)

# admin.site.register(Language)
# admin.site.register(CategoryDescription)
# admin.site.register(ProductDescription)
admin.site.register(Category)
admin.site.register(Product)
