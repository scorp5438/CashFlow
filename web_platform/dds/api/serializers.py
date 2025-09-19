from rest_framework import serializers

from ..models import (
    Category,
    Subcategory
)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Category.

    Предназначен для преобразования объектов Category в JSON и обратно.
    Используется в API endpoints для работы с категориями операций.

    Сериализует все поля модели:
        - id: идентификатор категории
        - type: связанный тип операции (ForeignKey)
        - category_name: название категории
    """
    class Meta:
        model = Category
        fields = '__all__'


class SubcategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Subcategory.

    Предназначен для преобразования объектов Subcategory в JSON и обратно.
    Используется в API endpoints для работы с подкатегориями операций.

    Сериализует все поля модели:
        - id: идентификатор подкатегории
        - category: связанная категория (ForeignKey)
        - subcategory_name: название подкатегории
    """
    class Meta:
        model = Subcategory
        fields = '__all__'