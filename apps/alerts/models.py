from django.db import models
from django.utils.timezone import now

from apps.core.models import BaseModel
from apps.products.models import Product

from utils.constants import STATUS_ACTIVE_ID, ALERT_STATUSES, STATUS_EXPIRED_ID


class Alert(BaseModel):
    status = models.IntegerField(choices=ALERT_STATUSES, default=STATUS_ACTIVE_ID)
    activation_date = models.DateTimeField(blank=True, null=True, db_index=True)
    days_to_activation = models.IntegerField(blank=True, null=True, db_index=True)
    days_since_activation = models.IntegerField(blank=True, null=True, db_index=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def update_days(self):
        """Método para actualizar los días basados en la fecha de activación"""
        if self.activation_date:
            today = now().date()
            activation_date = self.activation_date.date()
            self.days_to_activation = (activation_date - today).days if activation_date > today else 0
            self.days_since_activation = (today - activation_date).days if activation_date <= today else 0
            # update alert status
            # if today >= activation_date:
            #     self.status = STATUS_EXPIRED_ID
        else:
            self.days_to_activation = None
            self.days_since_activation = None

    class Meta:
        ordering = ['activation_date']