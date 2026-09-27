from django.urls import path

from apps.health.views import HealthView

urlpatterns = [
    path("health/", HealthView.as_view(), name="health"),
    path("health", HealthView.as_view()),
]
