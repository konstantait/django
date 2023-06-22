# import os

from django.db import models
# from django.conf import settings
from django_lifecycle import LifecycleModelMixin, hook, BEFORE_UPDATE # noqa

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

from core.settings import AUTH_USER_MODEL
from currencies.models import Currency

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
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        default_related_name = 'categories'

    def __str__(self):
        return self.name


class Product(
    LifecycleModelMixin,
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
    sku = models.CharField(max_length=64, unique=True)
    favorites = models.ManyToManyField(AUTH_USER_MODEL, blank=True, related_name='favorites') # noqa
    feedbacks = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField(Category, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,  default=Currency.get_default_id) # noqa
    # attributes = models.ManyToManyField(Attribute, blank=True)

    class Meta:
        default_related_name = 'products'

    def __str__(self):
        return self.name

    # @hook(BEFORE_UPDATE, when='image')
    # def after_update_signal(self):
    #     if self.initial_value('image'):
    #         if str(self.initial_value('image')) != 'placeholder.jpg':
    #             image_path = os.path.join(
    #                 settings.BASE_DIR,
    #                 settings.MEDIA_ROOT,
    #                 str(self.initial_value('image'))
    #             )
    #         try:
    #             os.remove(image_path)
    #         except (FileNotFoundError, OSError, IOError):
    #             ...

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

    def get_categories(self):
        return [
            category['name'] for category in (
                self.categories
                .all()
                .order_by('sort_order')
                .values('name')
            )
        ]
