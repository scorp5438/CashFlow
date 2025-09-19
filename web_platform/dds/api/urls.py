from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import (
    CategoryViewSet,
    SubcategoryViewSet
)

app_name = 'api-root'

router = DefaultRouter()

router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subcategory', SubcategoryViewSet, basename='subcategory')



urlpatterns = [
    path('', include(router.urls)),
]