from django.contrib import admin

from apps.hello.models import Greeting


@admin.register(Greeting)
class GreetingAdmin(admin.ModelAdmin):
    list_display = ("mensagem",)
