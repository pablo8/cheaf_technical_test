from datetime import datetime
import django_filters
from django.utils import timezone
from django_filters import rest_framework as filters


from apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    range_dates = filters.CharFilter(method='filter_range_dates')
    status = filters.CharFilter(method='filter_status')

    @staticmethod
    def filter_range_dates(queryset, name, value):
        try:
            # Separar las fechas
            start_date_str, end_date_str = value.split(",")

            # Convertir a datetime
            start_date = datetime.strptime(start_date_str, "%d/%m/%Y %H:%M")
            end_date = datetime.strptime(end_date_str, "%d/%m/%Y %H:%M")

            if timezone.is_naive(start_date):
                start_date = timezone.make_aware(start_date, timezone.get_current_timezone())
            if timezone.is_naive(end_date):
                end_date = timezone.make_aware(end_date, timezone.get_current_timezone())

            # Filtrar el queryset
            return queryset.filter(
                stock__gt=0,
                expiration_date__gte=start_date,
                expiration_date__lte=end_date
            )

        except ValueError:
            return queryset.none()

    @staticmethod
    def filter_status(queryset, name, value):
        try:
            return queryset.filter(alert__status=int(value))
        except ValueError:
            return queryset.none()

    class Meta:
        model = Product
        fields = []
