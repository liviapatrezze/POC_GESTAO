from rest_framework import serializers

from apps.items.models import Item


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "titulo", "descricao", "criado_em"]
        read_only_fields = ["id", "criado_em"]
