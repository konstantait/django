from django.db import models
from django.core.validators import MinValueValidator

from core.constants import MAX_DIGITS, DECIMAL_PLACES

from core.mixins.models import (
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
)


class Currency(
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    title = symbol_left = models.CharField(max_length=32, default='', blank=True) # noqa
    code = models.CharField(max_length=3, unique=True)
    symbol_left = models.CharField(max_length=12, default='', blank=True)
    symbol_right = models.CharField(max_length=12, default='', blank=True)
    decimal_place = models.PositiveIntegerField(default=2)

    rate = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    def __str__(self):
        return self.code
