# Importación de terceros
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Auth to handle public apis requests with DRF Allow Any permissions.
    """
    def authenticate(self, request):
        view = request.resolver_match.func.cls
        if view and AllowAny in view.permission_classes:
            return None  # Skip authentication for views with AllowAny permission
        return super().authenticate(request)
