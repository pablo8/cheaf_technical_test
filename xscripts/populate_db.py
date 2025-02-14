# Librerias propias de python
import argparse
import os
import sys
import random
from datetime import datetime

# Importación de terceros
import pytz
from faker import Faker
from dateutil.relativedelta import relativedelta

# Configuración de Django
project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaf_test_tecnico.settings")

import django
django.setup()

# Importaciones de modulos internos del proyecto
from utils.constants import STATUS_EXPIRED_ID, STATUS_ACTIVE_ID
from apps.products.models import Product
from apps.alerts.models import Alert

fake = Faker()


def calculate_activation_dates(expiration_date):
    """Calcula las fechas de activación de las alertas basado en la fecha de expiración."""
    try:
        return (expiration_date - relativedelta(days=10)).astimezone(pytz.UTC), (
                expiration_date - relativedelta(days=5)).astimezone(pytz.UTC)
    except:
        return None, None


def generate_products_and_alerts(n, d_today, expiration_dates_range):
    """Genera productos y alertas en bulk de manera optimizada."""
    products = []
    alerts = []
    start_date = expiration_dates_range[0]
    end_date = expiration_dates_range[1]
    for ix, _ in enumerate(range(n)):
        name = fake.word(ext_word_list=[f'Product {ix}'])
        description = fake.word(ext_word_list=[f' Description for product {ix}'])
        stock = random.randint(1, 10)

        # Generar fecha de expiración aleatoria
        expiration_date = fake.date_time_between(start_date=start_date, end_date=end_date).astimezone(pytz.UTC)

        products.append(Product(
            name=name,
            description=description,
            stock=stock,
            expiration_date=expiration_date
        ))

    # Guardar los productos en bulk
    created_products = Product.objects.bulk_create(products)

    # Generar las alertas en memoria
    for product in created_products:
        activation_date_alert_1, activation_date_alert_2 = calculate_activation_dates(product.expiration_date)

        for activation_date in [activation_date_alert_1, activation_date_alert_2]:
            if activation_date:
                activation_date_only = activation_date.date()

                # Calcular días antes y después de la activación
                days_to_activation = (activation_date_only - d_today).days if activation_date_only > d_today else 0
                days_since_activation = (d_today - activation_date_only).days if activation_date_only <= d_today else 0

                status = STATUS_ACTIVE_ID if activation_date_only >= d_today else STATUS_EXPIRED_ID
                alerts.append(Alert(
                    status=status,
                    activation_date=activation_date,
                    days_to_activation=days_to_activation,
                    days_since_activation=days_since_activation,
                    product=product
                ))

    # Guardar las alertas en bulk
    Alert.objects.bulk_create(alerts)


def main():
    parser = argparse.ArgumentParser(
        description="Script para agregar masivamente datos de pruebas de productos y alertas")
    parser.add_argument('total_productos', nargs='?', type=int, help='Total de registros de productos')

    args = parser.parse_args()

    print("Añadiendo datos de prueba...")
    # Representa la cantidad productos
    n_product = args.total_productos if args.total_productos else 1000
    # Representa el rango de fechas de expiración de los productos
    range_date = [
        datetime(2025, 2, 1, 12, 0, 0, tzinfo=pytz.UTC),
        datetime(2025, 2, 15, 12, 0, 0, tzinfo=pytz.UTC)
    ]
    # x = 1 Representa status de alertas activas
    # x = 2 Representa status de alertas expiradas
    # x = 3 Representa status de alertas mitad activas y mitad expiradas
    x = 1  # El while es para evitar correlo manualmente
    while x <= 3:
        if x == 1:
            # Alert active status
            date_today = datetime(2025, 1, 15, 12, 0, 0, tzinfo=pytz.UTC).date()
            msg = 'activas'
        elif x == 2:
            # Alert expired status
            date_today = datetime(2025, 2, 16, 12, 0, 0, tzinfo=pytz.UTC).date()
            msg = 'expiradas'
        else:
            # Alert active and expired (mixin)
            date_today = datetime(2025, 2, 7, 12, 0, 0, tzinfo=pytz.UTC).date()
            msg = 'mezcladas'

        print(f"Insertando {n_product} productos con alertas {msg}")
        generate_products_and_alerts(n_product, date_today, range_date)
        x += 1

    print("Base de datos cargada con éxito.")


if __name__ == "__main__":
    main()
