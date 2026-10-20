from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "slug", "category", "price", "in_stock", "created_at"]
    list_filter = ["in_stock", "category"]
    search_fields = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}
