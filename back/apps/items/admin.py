from django.contrib import admin

from apps.items.models import Item


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("titulo", "criado_em")
    search_fields = ("titulo", "descricao")
