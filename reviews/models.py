from django.db import models
from django.core.cache import cache
from django_lifecycle import (
    LifecycleModelMixin,
    hook,
    AFTER_CREATE,
    AFTER_UPDATE
)

from core.mixins.models import (
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
)
from core.enums import (
    CacheKeys,
    RatingTypes
)
from core.settings import AUTH_USER_MODEL

from catalog.models import Product


class Review(
    LifecycleModelMixin,
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE) # noqa
    product = models.ForeignKey(Product, on_delete=models.CASCADE) # noqa
    rating = models.PositiveSmallIntegerField(choices=RatingTypes.choices, default=RatingTypes.EXCELLENT) # noqa
    text = models.TextField(blank=False, null=False)

    class Meta:
        default_related_name = 'reviews'

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_review_create_or_update(self):
        cache.delete(CacheKeys.REVIEWS_ALL)
