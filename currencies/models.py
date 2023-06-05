from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django_lifecycle import (
    LifecycleModelMixin,
    hook,
    AFTER_UPDATE,
    AFTER_CREATE
)

from core.constants import MAX_DIGITS, DECIMAL_PLACES_CURRENCY
from core.mixins.models import (
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
)

from core.enums import CacheKeys


class Currency(
    LifecycleModelMixin,
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    title = models.CharField(max_length=32, default='', blank=True) # noqa
    code = models.CharField(max_length=3, unique=True)
    symbol_left = models.CharField(max_length=12, default='', blank=True)
    symbol_right = models.CharField(max_length=12, default='', blank=True)
    decimal_place = models.PositiveIntegerField(default=2)
    rate = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES_CURRENCY,
        default=1
    )

    def __str__(self):
        return self.code

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_create_or_update_signal(self):
        cache.delete(CacheKeys.CURRENCIES_ALL)
