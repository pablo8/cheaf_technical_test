import sys

# Importación de terceros
from django.db import transaction
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

# Importaciones de modulos internos del proyecto
from apps.alerts.filters import AlertFilter
from apps.alerts.models import Alert
from apps.alerts.serializers import AlertSerializer
from utils.helpers import convert_str_to_datetime
from utils.mixins import CachedViewMixin


class AlertViewSet(
    CachedViewMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = AlertSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AlertFilter

    def get_queryset(self):
        return Alert.objects.all().select_related('product')

    def update(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                activation_date = request.data.get("activation_date")
                obj_status = request.data.get("status")
                days_to_activation = request.data.get("days_to_activation")
                days_since_activation = request.data.get("days_since_activation")

                if not activation_date:
                    return Response(
                        {"result": "ERROR", "detail": "activation_date is required!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                activation_date = convert_str_to_datetime(activation_date)
                if activation_date is None:
                    return Response(
                        {"result": "ERROR", "detail": "format error, activation_date format is dd/mm/yyyy hh:mm!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if timezone.is_naive(activation_date):
                    activation_date = timezone.make_aware(activation_date, timezone.get_current_timezone())

                alert = Alert.objects.get(id=kwargs["pk"])
                alert.status = int(obj_status['id'])
                alert.days_to_activation = days_to_activation
                alert.days_since_activation = days_since_activation
                alert.activation_date = activation_date
                alert.update_days()
                alert.save()

            return Response(
                {
                    "result": "OK",
                    "detail": "Alert updated!",
                },
                status=status.HTTP_200_OK,
            )
        except Exception as ex:
            return Response(
                {
                    "result": "ERROR",
                    "detail": f"{ex.__str__()},LineNo: {sys.exc_info()[2].tb_lineno}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )