from django.urls import path

from .views import (
    IndexView,
    CreateDdsView,
    UpdateDdsView,
    DeleteDdsView,
    StatusesView,
    CreateStatusView,
    UpdateStatusView,
    DeleteStatusView,
    TypesView,
    CreateTypeView,
    UpdateTypeView,
    DeleteTypeView,
    CategoriesView,
    CreateCategoryView,
    UpdateCategoryView,
    DeleteCategoryView,
    SubcategoriesView,
    CreateSubcategoryView,
    UpdateSubcategoryView,
    DeleteSubcategoryView,
)

app_name = 'dds'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create/dds/', CreateDdsView.as_view(), name='create_dds'),
    path('update/dds/<int:pk>', UpdateDdsView.as_view(), name='update_dds'),
    path('delete/dds/<int:pk>', DeleteDdsView.as_view(), name='delete_dds'),

    path('statuses/', StatusesView.as_view(), name='statuses'),
    path('create/status/', CreateStatusView.as_view(), name='create_status'),
    path('update/status/<int:pk>', UpdateStatusView.as_view(), name='update_status'),
    path('delete/status/<int:pk>', DeleteStatusView.as_view(), name='delete_status'),

    path('types/', TypesView.as_view(), name='types'),
    path('create/type/', CreateTypeView.as_view(), name='create_type'),
    path('update/type/<int:pk>', UpdateTypeView.as_view(), name='update_type'),
    path('delete/type/<int:pk>', DeleteTypeView.as_view(), name='delete_type'),

    path('categories/', CategoriesView.as_view(), name='categories'),
    path('create/category/', CreateCategoryView.as_view(), name='create_category'),
    path('update/category/<int:pk>', UpdateCategoryView.as_view(), name='update_category'),
    path('delete/category/<int:pk>', DeleteCategoryView.as_view(), name='delete_category'),

    path('subcategories/', SubcategoriesView.as_view(), name='subcategories'),
    path('create/subcategory/', CreateSubcategoryView.as_view(), name='create_subcategory'),
    path('update/subcategory/<int:pk>', UpdateSubcategoryView.as_view(), name='update_subcategory'),
    path('delete/subcategory/<int:pk>', DeleteSubcategoryView.as_view(), name='delete_subcategory'),
]
