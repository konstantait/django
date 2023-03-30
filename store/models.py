from django.db import models
from django.core.validators import MinValueValidator

from core.mixins.models import \
    BaseUUID, \
    BaseDateAddedModified, \
    BaseImageStatusSortOrder, \
    BaseDescription
from core.constants import MAX_DIGITS, DECIMAL_PLACES


class Language(BaseUUID,
               BaseImageStatusSortOrder):

    name = models.CharField(max_length=32)
    code = models.CharField(max_length=5)
    locale = models.CharField(max_length=255)


class Category(BaseUUID,
               BaseDateAddedModified,
               BaseImageStatusSortOrder):
    pass
    # parent (id parent)


class CategoryDescription(BaseUUID, BaseDescription):

    category = models.ForeignKey(Category,
                                 blank=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Language,
                                 blank=True, on_delete=models.CASCADE)


class Product(BaseUUID,
              BaseDateAddedModified,
              BaseImageStatusSortOrder):

    model = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )


class ProductDescription(BaseUUID, BaseDescription):
    product = models.ForeignKey(Product,
                                blank=True, on_delete=models.CASCADE)
    language = models.ForeignKey(Language,
                                 blank=True, on_delete=models.CASCADE)


class Discount(BaseUUID):
    class DiscountType(models.IntegerChoices):
        CASH = 0, 'cash'
        PERCENT = 1, "percent"

    amount = models.PositiveIntegerField()
    code = models.CharField(max_length=64)
    status = models.BooleanField(default=True)
    type = models.PositiveSmallIntegerField(
        choices=DiscountType.choices,
        default=DiscountType.CASH)
