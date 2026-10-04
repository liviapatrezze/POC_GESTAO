from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class HelloViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_hello_returns_seeded_message(self) -> None:
        response = self.client.get("/api/hello/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"mensagem": "Hello, world"})
