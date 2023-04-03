from django.db import models

from core.mixins.models import (
    BaseUUID,
    BaseDescription,
    BaseImage,
    BaseQuantityPrice,
    BaseStatusSortOrder,
    BaseDateAddedModified
)


class Category(
    BaseUUID,
    BaseDescription,  # make a separate table language_id, category_id
    BaseImage,
    BaseStatusSortOrder,
    BaseDateAddedModified
):
    # parent_id
    def __str__(self):
        return f"{self.name}"


class Product(
    BaseUUID,
    BaseDescription,  # make a separate table language_id, product_id
    BaseImage,
    BaseQuantityPrice,
    BaseStatusSortOrder,
    BaseDateAddedModified
):
    model = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    # stock_status_id
    # manufacture_id
    # categories = models.ManyToManyField(Category, blank=True)
    # products = models.ManyToManyField('store.Product', blank=True)

    def __str__(self):
        return f"{self.name} {self.model} ({self.sku})"


# class Language(BaseUUID, BaseImageStatusSortOrder):
#     name = models.CharField(max_length=32)
#     code = models.CharField(max_length=5)
#     locale = models.CharField(max_length=255)

# class CategoryDescription(
#     BaseUUID,
#     BaseDescription
# ):
#     category = models.ForeignKey(
#         Category,
#         blank=True,
#         on_delete=models.CASCADE
#     )
#     language = models.ForeignKey(
#         Language,
#         blank=True,
#         on_delete=models.CASCADE
#     )


# class ProductDescription(
#     BaseUUID,
#     BaseDescription
# ):
#     product = models.ForeignKey(
#         Product,
#         blank=True,
#         on_delete=models.CASCADE
#     )
#     language = models.ForeignKey(
#         Language,
#         blank=True,
#         on_delete=models.CASCADE
#     )
