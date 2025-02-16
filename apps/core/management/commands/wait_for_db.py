import time
from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    help = "Espera hasta que la base de datos esté lista"

    def handle(self, *args, **kwargs):
        self.stdout.write("Esperando la base de datos...")
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections["default"]
            except OperationalError:
                self.stdout.write("Base de datos no disponible, reintentando en 2 segundos...")
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("Base de datos disponible!"))
