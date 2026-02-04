from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ProductViewSet, SupplierViewSet

router = DefaultRouter()
router.register(r"suppliers", SupplierViewSet, basename="supplier")
router.register(r"products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
