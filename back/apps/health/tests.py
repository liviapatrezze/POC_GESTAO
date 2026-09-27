from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class HealthViewTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_health_returns_ok(self) -> None:
        response = self.client.get("/api/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"status": "ok"})
