from rest_framework import routers
from apps.core.viewsets import UserViewSet

core_router = routers.SimpleRouter()

core_router.register(r"user", UserViewSet, basename="user")

