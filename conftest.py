import os
import django


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cheaf_test_tecnico.settings')
    django.setup()
