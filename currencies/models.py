from django.db import models
from django.core.cache import cache
from django.core.validators import MinValueValidator
from django_lifecycle import (
    LifecycleModelMixin,
    hook,
    AFTER_UPDATE,
    AFTER_CREATE
)

from core.mixins.models import (
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
)

from core.enums import CacheKeys
from core.settings import DEFAULT_CURRENCY


class Currency(
    LifecycleModelMixin,
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    code = models.CharField(max_length=3, unique=True)
    symbol = models.CharField(max_length=12, default='', blank=True)
    rate = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=32,
        decimal_places=4,
        default=1
    )

    @classmethod
    def get_default_id(cls):
        currency, _ = cls.objects.get_or_create(code=DEFAULT_CURRENCY)
        return currency.id

    def __str__(self):
        return self.code

    @hook(AFTER_CREATE)
    @hook(AFTER_UPDATE)
    def after_create_or_update_signal(self):
        cache.delete(CacheKeys.CURRENCIES_ALL)
