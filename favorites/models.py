# from django.db import models
#
# from core.settings import AUTH_USER_MODEL
# from core.mixins.models import BaseUUID
# from catalog.models import Product


# class Favorite(BaseUUID):
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
#
#     class Meta:
#         unique_together = ('product', 'user')
#         default_related_name = 'favorites'
