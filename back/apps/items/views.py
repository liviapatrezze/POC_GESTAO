from rest_framework import viewsets

from apps.items.models import Item
from apps.items.serializers import ItemSerializer


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
