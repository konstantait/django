from django.db import models
from django.core.validators import MinValueValidator

from core.model_choices import DiscountTypes

from core.mixins.models import (
    BaseUUID,
    BaseDateAddedModified,
    BaseImageStatusSortOrder,
    BaseDescription
)

from core.constants import MAX_DIGITS, DECIMAL_PLACES


class Category(
    BaseUUID,
    BaseDescription,  # make a separate table language_id, category_id
    BaseDateAddedModified,
    BaseImageStatusSortOrder
):
    pass
    # parent_id


class Product(
    BaseUUID,
    BaseDescription,  # make a separate table language_id, product_id
    BaseDateAddedModified,
    BaseImageStatusSortOrder
):
    model = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    # manufacture_id
    # categories = models.ManyToManyField(Category, blank=True)
    # products = models.ManyToManyField('store.Product', blank=True)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
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


class Discount(
    BaseUUID
):
    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.CASH
    )
