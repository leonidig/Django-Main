from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.filters import OrderingFilter, SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser, AllowAny
from ..models import Product
from ..serializers import ProductSerializer
from ..filters import ProductFilter


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']
    ordering_fields = ['price','rating']
    
    def get_permissions(self):
        if self.action in ["create","update","partial_update","destroy"]:
            return [IsAdminUser()]
        else:
            return [AllowAny()]