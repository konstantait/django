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


class AttributeGroup(
    BaseUUID,
    BaseName,
    BaseSortOrder
):
    def __str__(self):
        return self.name


class Attribute(
    BaseUUID,
    BaseName,
    BaseSortOrder
):
    attribute_group = models.ForeignKey(
        AttributeGroup,
        on_delete=models.CASCADE,
        related_name='attributes',
        verbose_name='Group'
    )

    def __str__(self):
        return self.name


class Category(
    BaseUUID,
    BaseName,
    BaseDescription,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
):
    def __str__(self):
        return self.name


class Product(
    BaseUUID,
    BaseName,
    BaseDescription,
    BaseImage,
    BaseQuantityPrice,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
):
    model = models.CharField(max_length=64, default='')
    sku = models.CharField(max_length=64, default='')

    categories = models.ManyToManyField(
        Category,
        related_name='products',
    )

    attributes = models.ManyToManyField(
        Attribute,
        related_name='products',
    )

    def __str__(self):
        return self.name

    def get_categories(self):
        return [
            category['name'] for category in (
                self.categories
                .all()
                .order_by('sort_order')
                .values('name')
            )
        ]

    def get_attributes(self):
        return [
            attribute['attribute_group__name'] +
            ':' +
            attribute['name'] for attribute in (
                self.attributes
                .select_related('attribute_group')
                .order_by('attribute_group__sort_order')
                .values('attribute_group__name', 'name')
            )
        ]


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
