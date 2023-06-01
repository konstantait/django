import uuid

from os import path
from django.db import models
from django.core.validators import MinValueValidator


from core.enums import StatusTypes
from core.constants import MAX_DIGITS, DECIMAL_PLACES


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f'products/images/{str(instance.pk)}{extension}'


class BaseUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseName(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True


class BaseSlug(models.Model):
    slug = models.SlugField(max_length=100, unique=True)

    class Meta:
        abstract = True


class BaseDescription(models.Model):
    description = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True


class BaseImage(models.Model):
    image = models.ImageField(upload_to=upload_to, default='placeholder.jpg') # noqa

    class Meta:
        abstract = True


class BaseStatus(models.Model):
    status = models.PositiveSmallIntegerField(
        choices=StatusTypes.choices,
        default=StatusTypes.ENABLED
    )

    class Meta:
        abstract = True


class BaseSortOrder(models.Model):
    sort_order = models.IntegerField(
        default=0,
        verbose_name='Sort'
    )

    class Meta:
        abstract = True


class BaseDateAdded(models.Model):
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Added'
    )

    class Meta:
        abstract = True


class BaseDateAddedModified(
    BaseDateAdded,
    models.Model
):
    date_modified = models.DateTimeField(
        auto_now=True,
        verbose_name='Modified'
    )

    class Meta:
        abstract = True


class BaseDateStartEnd(models.Model):
    date_start = models.DateTimeField()
    date_end = models.DateTimeField()

    class Meta:
        abstract = True


class BaseQuantityPrice(models.Model):
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(
        validators=[MinValueValidator(0)],
        max_digits=MAX_DIGITS,
        decimal_places=DECIMAL_PLACES,
        default=0
    )

    class Meta:
        abstract = True
