from django.contrib import admin

from store.models import (
    Language,
    Category,
    CategoryDescription,
    Product,
    ProductDescription
)


admin.site.register(Language)
admin.site.register(Category)
admin.site.register(CategoryDescription)
admin.site.register(Product)
admin.site.register(ProductDescription)
