import uuid

from django.db import models
from os import path


def upload_to(instance, filename):
    _name, extension = path.splitext(filename)
    return f"store/images/{str(instance.pk)}.{extension}"


class BaseUUID(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class BaseDateAddedModified(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class BaseImageStatusSortOrder(models.Model):
    image = models.ImageField(upload_to=upload_to)
    status = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)

    class Meta:
        abstract = True
