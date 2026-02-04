from rest_framework import viewsets
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ChainNode, Product
from .serializers import ChainNodeSerializer, ProductSerializer
from users.permissions import IsActiveStaff

class SupplierViewSet(viewsets.ModelViewSet):
    """
    CRUD для модели поставщика (ChainNode).
    Обновление debt запрещено через сериализатор.
    """
    queryset = ChainNode.objects.all()
    serializer_class = ChainNodeSerializer
    permission_classes = [IsActiveStaff]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["country", "city", "level"]
    search_fields = ['name', 'city', 'country']
    ordering_fields = ["name", "city", "debt", "created_at"]

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с продуктами"""

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["chain_node__country", "chain_node__city"]
    search_fields = ["name", "model", "chain_node__name"]
    ordering_fields = ["name", "model", "release_date"]

    def get_queryset(self):
        return Product.objects.select_related("chain_node")
