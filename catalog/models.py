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

from core.enums import (
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

    def __str__(self):
        return f"{self.name} {self.model} ({self.sku})"


class Review(
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    rating = models.PositiveSmallIntegerField(
        choices=RatingTypes.choices,
        default=RatingTypes.EXCELLENT
    )
    text = models.TextField(
        blank=False,
        null=False
    )
