import os
import django


# Configurar el entorno Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaf_test_tecnico.settings")
django.setup()

# Importar Celery y las tareas
from apps.alerts.tasks import update_alerts, notify_products_before_expiration




if __name__ == "__main__":
    simulate_notifications(days=7, step_minutes=1)
