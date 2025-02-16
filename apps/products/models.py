from django.core.exceptions import ValidationError
from django.db import models
from django.utils.timezone import now

from apps.core.models import BaseModel
from apps.products.managers import ProductManager
from utils.constants import STATUS_EXPIRED_ID


class Product(BaseModel):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(db_index=True)

    objects = ProductManager()

    def __str__(self):
        return self.name

    def clean(self):
        if self.expiration_date and self.expiration_date < now():
            raise ValidationError('La fecha de expiración no puede estar en el pasado')

    class Meta:
        ordering = ["expiration_date"]