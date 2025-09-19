from django.contrib import admin

from .models import (
    Status,
    Type,
    Category,
    Subcategory
)


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = 'pk', 'status_name'
    list_display_links = 'pk', 'status_name',


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = 'pk', 'type_name'
    list_display_links = 'pk', 'type_name',


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'category_name'
    list_display_links = 'pk', 'category_name',


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = 'pk', 'category', 'subcategory_name'
    list_display_links = 'pk', 'category', 'subcategory_name'
