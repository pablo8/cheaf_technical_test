import sys
# Si los datos son simples (dict, list, str), usa json o cache.set().
# Si se necesita almacenar objetos más complejos, usar pickle.
import pickle

from dateutil.relativedelta import relativedelta
from django.db import transaction
from django.core.cache import cache
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.alerts.models import Alert
from apps.products.filters import ProductFilter
from apps.products.models import Product
from apps.products.serializers import ProductSerializer
from utils.constants import STATUS_EXPIRED_ID, STATUS_ACTIVE_ID
from utils.helpers import convert_str_to_datetime, calculate_activation_dates
from utils.mixins import CachedViewMixin


class ProductViewSet(
    CachedViewMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def create(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                name = request.data.get("name")
                description = request.data.get("description")
                stock = request.data.get("stock", 0)

                expiration_date = request.data.get("expiration_date")
                if not expiration_date:
                    return Response(
                        {"result": "ERROR", "detail": "expiration_date is required!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                expiration_date = convert_str_to_datetime(expiration_date)
                if expiration_date is None:
                    return Response(
                        {"result": "ERROR", "detail": "format error, expiration_date format is dd/mm/yyyy hh:mm!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product = Product.objects.create(
                    name=name,
                    description=description,
                    stock=stock,
                    expiration_date=expiration_date
                )

                activation_date_alert_1, activation_date_alert_2 = calculate_activation_dates(expiration_date)

                # # # Create and link alerts
                alerts = [
                    Alert(activation_date=activation_date_alert_1, product=product),
                    Alert(activation_date=activation_date_alert_2, product=product)
                ]

                Alert.objects.bulk_create(alerts)

                # Actualización de los días
                for alert in alerts:
                    alert.update_days()
                    alert.save()

            return Response(
                {
                    "result": "OK",
                    "detail": "Product created!",
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

    def update(self, request, *args, **kwargs):
        try:
            with (transaction.atomic()):
                name = request.data.get("name")
                description = request.data.get("description")
                stock = request.data.get("stock")

                expiration_date = request.data.get("expiration_date")
                if not expiration_date:
                    return Response(
                        {"result": "ERROR", "detail": "expiration_date is required!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                expiration_date = convert_str_to_datetime(expiration_date)
                if expiration_date is None:
                    return Response(
                        {"result": "ERROR", "detail": "format error, expiration_date format is dd/mm/yyyy hh:mm!"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                product = Product.objects.get(id=kwargs["pk"])
                product.name = name
                product.description = description
                product.stock = stock

                if expiration_date != product.expiration_date:

                    alerts = Alert.objects.filter(product=product).order_by("activation_date")
                    # Caso 1 | Las dos alertas asociadas al producto están activas (no notificaron)
                    if all(alert.status == STATUS_ACTIVE_ID for alert in alerts):
                        alert_10_days = max(alerts, key=lambda a: a.activation_date)  # Mayor 10 días
                        alert_5_days = min(alerts, key=lambda a: a.activation_date)  # Menor 5 días

                    # Caso 2 | 1 alerta expiró (notifico, y seria la primera) y
                    # la otra alerta sigue activa (no notificó)
                    elif any(alert.status == STATUS_ACTIVE_ID for alert in alerts) and any(alert.status == STATUS_EXPIRED_ID for alert in alerts):
                        alert_5_days = next(alert for alert in alerts if alert.status == STATUS_ACTIVE_ID)
                        alert_10_days = None
                    else:
                        return Response(
                            {"result": "ERROR", "detail": "No hay alertas activas para actualizar."},
                            status=status.HTTP_400_BAD_REQUEST,
                        )

                    product.expiration_date = expiration_date
                    product.save()

                    alert_5_days.activation_date = expiration_date - relativedelta(days=5)
                    alert_5_days.update_days()
                    alert_5_days.save()

                    if alert_10_days is not None:
                        alert_10_days.activation_date = expiration_date - relativedelta(days=10)
                        alert_10_days.update_days()
                        alert_10_days.save()

            return Response(
                {
                    "result": "OK",
                    "detail": "Product updated!",
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

    @action(methods=["get"], detail=False, url_path="expiring")
    def expiring(self, request, *args, **kwargs):
        """
                  Se consideran el estado de expirado cuando al menos una de las alertas fue activada
                  caché ahora es gestionada automáticamente por CachedViewMixin.
                  """
        try:
            expired_products = Product.objects.with_at_least_one_expired_alert()
            page = self.paginate_queryset(expired_products)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(expired_products, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as ex:
            return Response(
                {
                    "result": "ERROR",
                    "detail": f"{ex.__str__()},LineNo: {sys.exc_info()[2].tb_lineno}",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
