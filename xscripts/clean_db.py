# Librerias propias de python
import os
import sys

# Configuración de Django
project_home = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_home)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cheaf_test_tecnico.settings")

import django
django.setup()

# Importaciones de modulos internos del proyecto
from apps.products.models import Product

if __name__ == '__main__':
    print("Limpiando base de datos..")
    Product.objects.all().delete()
    print("Limpieza finalizada..")
