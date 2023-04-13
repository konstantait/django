import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.mixins.models import (
    BaseUUID,
    BaseName,
    BaseQuantityPrice,
    BaseStatus,
    BaseDateStartEnd,
    BaseDateAdded,
    BaseDateAddedModified
)

from core.constants import MAX_DIGITS, DECIMAL_PLACES
from core.enums import (
    DiscountTypes,
    StatusTypes
)
from catalog.models import Product

User = get_user_model()


class Coupon(
    BaseUUID,
    BaseName,
    BaseStatus,
    BaseDateStartEnd,
    BaseDateAdded
):
    code = models.CharField(
        max_length=32,
        unique=True
    )
    discount_type = models.PositiveSmallIntegerField(
        choices=DiscountTypes.choices,
        default=DiscountTypes.FIXED
    )
    discount = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    @property
    def is_valid(self):
        is_valid = True
        if self.status == StatusTypes.DISABLED:
            is_valid = False
        if self.date_start:
            is_valid &= timezone.now() >= self.date_start
        if self.date_end:
            is_valid &= timezone.now() <= self.date_end
        return is_valid

    def __str__(self):
        return f"{self.name}"


class Order(
    BaseUUID,
    BaseStatus,
    BaseDateAddedModified
):
    invoice = models.PositiveSmallIntegerField(default=1)
    invoice_prefix = models.CharField(max_length=16, default='')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    total_cost = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        if self.coupon and self.coupon.is_valid:
            total_cost = (
                total_cost - self.coupon.discount
                if self.coupon.discount_type == DiscountTypes.FIXED else
                total_cost - (total_cost / 100 * self.coupon.discount)
                ).quantize(decimal.Decimal('.01'))
        return total_cost

    def __str__(self):
        return f"{self.invoice_prefix}-{self.invoice}"


class OrderItem(
    BaseUUID,
    BaseQuantityPrice
):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='order_items',
    )
    cost = models.DecimalField(
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    def get_cost(self):
        return self.quantity * self.price

    class Meta:
        unique_together = ('order', 'product')
