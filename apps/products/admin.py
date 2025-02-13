from apps.products.models import Product
from django.contrib import admin


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "stock", "expiration_date")
    search_fields = ("expiration_date", "stock")
    list_filter = ("name", "description")
    ordering = ("expiration_date",)
