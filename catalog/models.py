from django.db import models
from django.contrib.auth import get_user_model

from core.mixins.models import (
    BaseUUID,
    BaseName,
    BaseDescription,
    BaseImage,
    BaseQuantityPrice,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
)

from core.model_choices import (
    RatingTypes
)

User = get_user_model()


class Category(
    BaseUUID,
    BaseName,
    BaseDescription,  # make a separate table language_id, category_id
    BaseImage,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
):
    # parent_id
    def __str__(self):
        return f"{self.name}"


class Product(
    BaseUUID,
    BaseName,
    BaseDescription,  # make a separate table language_id, product_id
    BaseImage,
    BaseQuantityPrice,
    BaseStatus,
    BaseSortOrder,
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


class Review(
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    text = models.TextField(blank=False, null=False)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField(
        choices=RatingTypes.choices,
        default=RatingTypes.EXCELLENT
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='reviews',
    )

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
