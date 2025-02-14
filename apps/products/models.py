from django.apps import apps
from django.db import models

from apps.core.models import BaseModel
from apps.products.managers import ProductManager


class Product(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(db_index=True)

    objects = ProductManager()

    class Meta:
        ordering = ["expiration_date"]