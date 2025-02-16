from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea un superusuario si no existe"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_email = "a@a.com"
        admin_password = "123"
        admin_first_name = "Admin"
        admin_last_name = "User"

        if not User.objects.filter(email=admin_email).exists():
            User.objects.create_superuser(
                email=admin_email,
                password=admin_password,
                first_name=admin_first_name,
                last_name=admin_last_name
            )
            self.stdout.write(self.style.SUCCESS(f"Superusuario {admin_email} creado exitosamente."))
        else:
            self.stdout.write(self.style.WARNING("El superusuario ya existe."))
