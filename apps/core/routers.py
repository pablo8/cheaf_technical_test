from rest_framework_nested import routers

from apps.alerts.viewsets import AlertViewSet
from apps.core.viewsets import UserViewSet
from apps.products.viewsets import ProductViewSet

core_router = routers.SimpleRouter()

core_router.register(r"user", UserViewSet, basename="user")
core_router.register(r"alerts", AlertViewSet, basename="alerts")
core_router.register(r"products", ProductViewSet, basename="products")

# Anidamiento para formar la relacion entre productos y alertas
nested_router = routers.NestedSimpleRouter(core_router, r"products", lookup="product")
nested_router.register(r"alerts", AlertViewSet, basename="product-alerts")
