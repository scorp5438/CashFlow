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
    """
    ViewSet для получения списка категорий (Category)

    Особенности:
        - Только чтение
        - Оптимизированные запросы select_related('type')
        - Фильтрация по типу
    Пример запроса:
        - /category/?type=2
    В ответ вернутся категории, принадлежащие статусу с id 2
    "id": 1,
    "category_name": "Маркетинг",
    "type": 2

    "id": 2,
    "category_name": "Офис и администрирование",
    "type": 2
    """
    http_method_names = ['get', ]
    queryset = Category.objects.select_related('type').all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['type']


class SubcategoryViewSet(ModelViewSet):
    """
    ViewSet для получения списка подкатегорий (Subcategory)

    Особенности:
        - Только чтение
        - Оптимизированные запросы select_related('category')
        - Фильтрация по категории
    Пример запроса:
        - /subcategory/?category=3
    В ответ вернутся категории, принадлежащие категории с id 3
        "id": 5,
        "subcategory_name": "Хозяйственные товары",
        "category": 3

        "id": 6,
        "subcategory_name": "Продажа товара",
        "category": 3

        "id": 11,
        "subcategory_name": "Оказание услуги",
        "category": 3
    """
    http_method_names = ['get', ]
    queryset = Subcategory.objects.select_related('category').all()
    serializer_class = SubcategorySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category']
