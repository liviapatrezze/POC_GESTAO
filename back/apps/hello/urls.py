from django.urls import path

from apps.hello.views import HelloView

urlpatterns = [
    path("hello/", HelloView.as_view(), name="hello"),
    path("hello", HelloView.as_view()),
]
