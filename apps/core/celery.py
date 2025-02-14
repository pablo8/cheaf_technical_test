import os
import platform
from celery import Celery

from celery.schedules import crontab
# Configurar Django antes de cargar Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaf_test_tecnico.settings")

app = Celery("cheaf_test_tecnico")

# Cargar configuración desde settings.py
app.config_from_object("django.conf:settings", namespace="CELERY")

# Detectar si estamos en Windows y forzar `solo` como pool
if platform.system() == "Windows":
    app.conf.worker_pool = "solo"

# Descubrir tareas automáticamente
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "update-alerts-every-24h": {
        "task": "apps.alerts.tasks.update_alerts",
        "schedule": crontab(minute=0, hour=0),  # Análogo en linux 0 0 * * * /ruta/al/tarea (todas las medias noche)
    },
}

app.conf.update(
    broker_connection_retry_on_startup=True,
)
