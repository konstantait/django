import decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from core.mixins.models import (
    BaseUUID,
    BaseQuantityPrice,
    BaseDateAdded,
    BaseDateAddedModified
)

from core.constants import MAX_DIGITS, DECIMAL_PLACES
from core.model_choices import DiscountTypes
from catalog.models import Product

User = get_user_model()


class Coupon(
    BaseUUID,
    BaseDateAdded
):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=32,
        unique=True
    )
    status = models.BooleanField(
        default=True
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
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(auto_now=True)

    @property
    def is_valid(self):
        is_valid = self.status
        if self.date_start:
            is_valid &= timezone.now() >= self.date_start
        if self.date_end:
            is_valid &= timezone.now() <= self.date_end
        return is_valid


class CouponHistory:
    pass


class Order(
    BaseUUID,
    BaseDateAddedModified
):
    invoice = models.PositiveSmallIntegerField(default=1)
    invoice_prefix = models.CharField(max_length=16)
    # store_id
    # customer_id
    # customer_group_id
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    # payment fields
    # shipping fields
    # order_status_id
    # is_active = models.BooleanField(default=True)
    # is_paid = models.BooleanField(default=False)

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
        return self.cost * self.price

    class Meta:
        unique_together = ('order', 'product')
