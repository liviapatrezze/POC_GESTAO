from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from apps.items.models import Item


class ItemApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_item_without_trailing_slash(self) -> None:
        response = self.client.post(
            "/api/items",
            {"titulo": "Sem barra", "descricao": ""},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["titulo"], "Sem barra")

    def test_create_and_list_item(self) -> None:
        create_response = self.client.post(
            "/api/items/",
            {"titulo": "Primeiro", "descricao": "Exemplo"},
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(create_response.json()["titulo"], "Primeiro")

        list_response = self.client.get("/api/items/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(list_response.json()), 1)

    def test_retrieve_update_and_delete_item(self) -> None:
        item = Item.objects.create(titulo="Original", descricao="Antes")

        retrieve_response = self.client.get(f"/api/items/{item.id}/")
        self.assertEqual(retrieve_response.status_code, status.HTTP_200_OK)

        update_response = self.client.patch(
            f"/api/items/{item.id}/",
            {"titulo": "Atualizado"},
            format="json",
        )
        self.assertEqual(update_response.status_code, status.HTTP_200_OK)
        self.assertEqual(update_response.json()["titulo"], "Atualizado")
        self.assertEqual(update_response.json()["descricao"], "Antes")

        delete_response = self.client.delete(f"/api/items/{item.id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=item.id).exists())
