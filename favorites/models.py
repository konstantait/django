from django.db import models
from django.contrib.auth import get_user_model

from core.mixins.models import (
    BaseUUID,
)

from catalog.models import Product

User = get_user_model()


class Favorite(BaseUUID):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def add(self, user_id, product_id):
        pass
