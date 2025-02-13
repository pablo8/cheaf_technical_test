from apps.alerts.models import Alert
from django.contrib import admin


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "activation_date", "days_to_activation", "days_since_activation", "product__name")
    search_fields = ("status", "activation_date")
    list_filter = ("status", "activation_date")
    ordering = ("product__name", "activation_date",)
