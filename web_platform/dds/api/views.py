from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .serializers import (
    CategorySerializer,
    SubcategorySerializer
)
from ..models import (
    Category,
    Subcategory
)


class CategoryViewSet(ModelViewSet):
    http_method_names = ['get',]
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']

class SubcategoryViewSet(ModelViewSet):
    http_method_names = ['get',]
    queryset = Subcategory.objects.select_related('category').all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']