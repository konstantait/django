from django.db import models
from django.contrib.auth.models import User

from core.mixins.models import (
    BaseUUID,
)


class Profile(BaseUUID):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.TextField(max_length=11, blank=True)
    location = models.CharField(max_length=100, blank=True)
    shipping = models.CharField(max_length=100, blank=True)
