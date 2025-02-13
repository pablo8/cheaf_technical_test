from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    stock = models.IntegerField(default=0)
    expiration_date = models.DateTimeField(db_index=True)

    class Meta:
        ordering = ["expiration_date"]