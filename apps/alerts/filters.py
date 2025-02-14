# Importación de terceros
import django_filters
from django_filters import filters
# Importaciones de modulos internos del proyecto
from apps.alerts.models import Alert


class AlertFilter(django_filters.FilterSet):
    status = filters.CharFilter(method='filter_status')

    @staticmethod
    def filter_status(queryset, name, value):
        try:
            return queryset.filter(status=int(value))
        except ValueError:
            return queryset.none()

    class Meta:
        model = Alert
        fields = []
