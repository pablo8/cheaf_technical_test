from django.db import models
from django.db.models import Exists, OuterRef
from django.apps import apps

from utils.constants import STATUS_EXPIRED_ID


class ProductManager(models.Manager):
    """Manager para optimizar consultas sobre productos."""

    def with_at_least_one_expired_alert(self):
        """
        Retorna productos que tienen al menos 1 alerta expirada.
        Usa `Exists()` para mejorar el rendimiento y evitar escaneos innecesarios.
        """
        Alert = apps.get_model('alerts', 'Alert')

        expired_alerts_qs = Alert.objects.filter(
            product=OuterRef('pk'),
            status=STATUS_EXPIRED_ID
        ).values('id')[:1]

        return self.get_queryset().filter(Exists(expired_alerts_qs))
