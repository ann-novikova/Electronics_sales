from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import ChainNode, Product

@admin.register(ChainNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = ["name", "level", "city", "supplier_link", "debt", "created_at"]
    list_filter = ["city", "country", "level"]
    search_fields = ["name", "city"]
    actions = ["clear_debt"]

    def supplier_link(self, obj):
        if obj.supplier:
            url = f"/admin/network/networknode/{obj.supplier.pk}/change/"
            return format_html('{}', url, obj.supplier.name)
        return '-'

    supplier_link.short_description = 'Поставщик'


    def clear_debt(self, request, queryset):
        updated = queryset.update(debt=0)
        self.message_user(request, f"Задолженность очищена для {updated} объектов")

    clear_debt.short_description = "Очистить задолженность перед поставщиком"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'chain_node', 'release_date')
    list_filter = ('release_date',)
    search_fields = ('name', 'model', 'chain_node__name')
