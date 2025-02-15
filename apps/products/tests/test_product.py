import pytest
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from datetime import timedelta
from apps.products.models import Product


@pytest.mark.django_db
def test_create_valid_product():
    """Verificar que un producto se cree correctamente"""
    product = Product.objects.create(
        name="Producto de prueba",
        description="Descripción del producto",
        stock=10,
        expiration_date=now() + timedelta(days=30)
    )

    assert product.id is not None
    assert product.name == "Producto de prueba"
    assert product.stock == 10
    assert product.expiration_date is not None


@pytest.mark.django_db
def test_expiration_date_cannot_be_past():
    """Verificar que un producto no pueda tener fecha de expiración en el pasado"""
    with pytest.raises(ValidationError):
        product = Product(
            name="Producto vencido",
            description="Este producto tiene una fecha de expiración inválida",
            stock=5,
            expiration_date=now() - timedelta(days=10)
        )
        product.full_clean()  # Forzar la validación


@pytest.mark.django_db
def test_product_string_representation():
    """Verificar la representación en string del producto"""
    product = Product.objects.create(
        name="Producto Test",
        description="Un producto de prueba",
        stock=10,
        expiration_date=now() + timedelta(days=30)
    )
    assert str(product) == "Producto Test"
