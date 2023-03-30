from django.db import models

from core.mixins.models import \
    BaseUUID, \
    BaseDateAddedModified, \
    BaseImageStatusSortOrder


class Product(BaseUUID,
              BaseDateAddedModified,
              BaseImageStatusSortOrder):

    model = models.CharField(max_length=64)
    sku = models.CharField(max_length=64)
