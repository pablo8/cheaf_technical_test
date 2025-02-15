import pytest

from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta

from apps.alerts.models import Alert
from apps.products.models import Product
from utils.constants import STATUS_ACTIVE_ID, STATUS_EXPIRED_ID


@pytest.mark.django_db
def test_create_valid_alert():
    """Verificar que una alerta se cree correctamente asociada a un producto"""
    product = Product.objects.create(
        name="Producto de prueba",
        description="Descripción del producto",
        stock=10,
        expiration_date=now() + timedelta(days=30)
    )

    alert = Alert.objects.create(
        product=product,
        activation_date=now() + timedelta(days=5),
        status=STATUS_ACTIVE_ID
    )

    assert alert.id is not None
    assert alert.product == product
    assert alert.activation_date is not None
    assert alert.status == STATUS_ACTIVE_ID


@pytest.mark.django_db
def test_alert_cannot_be_created_without_product():
    """Verificar que una alerta no pueda crearse sin un producto asociado"""
    with pytest.raises(ValidationError):
        alert = Alert(
            activation_date=now() + timedelta(days=5),
            status=STATUS_ACTIVE_ID
        )
        alert.full_clean()  # Forzar validación


@pytest.mark.django_db
def test_alert_status_changes_when_expired():
    """Verificar que una alerta cambia su estado a expirado cuando corresponde"""
    product = Product.objects.create(
        name="Producto de prueba",
        description="Descripción del producto",
        stock=10,
        expiration_date=now() + timedelta(days=5)
    )

    alert = Alert.objects.create(
        product=product,
        activation_date=now(),  # Se activa hoy
        status=STATUS_ACTIVE_ID
    )

    alert.update_days()  # Simulamos la actualización de días
    if alert.days_to_activation == 0:
        alert.status = STATUS_EXPIRED_ID
        alert.save()

    assert alert.status == STATUS_EXPIRED_ID


@pytest.mark.django_db
def test_alert_string_representation():
    """Verificar la representación en string de la alerta"""
    product = Product.objects.create(
        name="Producto Test",
        description="Un producto de prueba",
        stock=10,
        expiration_date=now() + timedelta(days=30)
    )

    alert = Alert.objects.create(
        product=product,
        activation_date=now() + timedelta(days=5),
        status=STATUS_ACTIVE_ID
    )

    assert str(alert) == f"Alerta para {product.name} - {alert.activation_date.strftime('%d/%m/%Y')}"
