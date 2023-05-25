from django.db import models

from core.mixins.models import (
    BaseUUID,
    BaseName,
    BaseSlug,
    BaseDescription,
    BaseImage,
    BaseQuantityPrice,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
)

# from core.constants import (
#     CSV_IN_FIELD_ATTR_DELIMITER
# )

from core.settings import AUTH_USER_MODEL


# class AttributeGroup(
#     BaseUUID,
#     BaseName,
#     BaseSortOrder
# ):
#     def __str__(self):
#         return self.name
#
#
# class Attribute(
#     BaseUUID,
#     BaseName,
#     BaseSortOrder
# ):
#     attribute_group = models.ForeignKey(
#         AttributeGroup,
#         on_delete=models.CASCADE,
#         related_name='attributes',
#         verbose_name='Group'
#     )
#
#     def __str__(self):
#         return self.name


class Category(
    BaseUUID,
    BaseName,
    BaseSlug,
    BaseDescription,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
):
    class Meta:
        default_related_name = 'categories'

    def __str__(self):
        return self.name


class Product(
    BaseUUID,
    BaseName,
    BaseSlug,
    BaseDescription,
    BaseImage,
    BaseQuantityPrice,
    BaseStatus,
    BaseSortOrder,
    BaseDateAddedModified
):
    model = models.CharField(max_length=64, default='', blank=True)
    sku = models.CharField(max_length=64, unique=True)
    bookmarked_by = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='favorites') # noqa
    bookmarks_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, blank=True)
    # attributes = models.ManyToManyField(Attribute, blank=True)

    class Meta:
        default_related_name = 'products'

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

    # def get_attributes(self):
    #     return [
    #         attribute['attribute_group__name'] +
    #         CSV_IN_FIELD_ATTR_DELIMITER +
    #         attribute['name'] for attribute in (
    #             self.attributes
    #             .select_related('attribute_group')
    #             .order_by('attribute_group__sort_order')
    #             .values('attribute_group__name', 'name')
    #         )
    #     ]
