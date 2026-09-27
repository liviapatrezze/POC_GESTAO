from django.urls import path

from apps.items.views import ItemViewSet

item_list = ItemViewSet.as_view({"get": "list", "post": "create"})
item_detail = ItemViewSet.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "patch": "partial_update",
        "delete": "destroy",
    }
)

urlpatterns = [
    path("items/", item_list, name="item-list"),
    path("items", item_list),
    path("items/<int:pk>/", item_detail, name="item-detail"),
    path("items/<int:pk>", item_detail),
]
