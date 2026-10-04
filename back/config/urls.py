from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.health.urls")),
    path("api/", include("apps.hello.urls")),
    path("api/", include("apps.items.urls")),
]
