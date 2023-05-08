from django.db import models
from django.core.cache import cache
from django.contrib.auth import get_user_model
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
    RatingTypes
)

from catalog.models import Product

User = get_user_model()


class Review(
    LifecycleModelMixin,
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

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_review_create_or_update(self):
        print('clear cache')
        cache.delete('reviews:all')
