import uuid

from os import path
from django.db import models
from django.core.validators import MinValueValidator


from core.model_choices import StatusTypes
from core.constants import MAX_DIGITS, DECIMAL_PLACES


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f"store/images/{str(instance.pk)}.{extension}"


class BaseUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseName(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class BaseDescription(models.Model):
    description = models.TextField(blank=True, null=True)
    # tag = models.TextField(blank=True)
    # meta_title = models.CharField(max_length=255)
    # meta_description = models.CharField(max_length=255)
    # meta_keyword = models.CharField(max_length=255)

    class Meta:
        abstract = True


class BaseImage(models.Model):
    image = models.ImageField(upload_to=upload_to)

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
    sort_order = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseDateAdded(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class BaseDateAddedModified(
    BaseDateAdded,
    models.Model
):
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseDateStartEnd(models.Model):
    date_start = models.DateTimeField(auto_now_add=True)
    date_end = models.DateTimeField(auto_now=True)

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
