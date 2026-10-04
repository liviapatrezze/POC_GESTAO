from django.db import migrations


def seed(apps, schema_editor):
    Greeting = apps.get_model("hello", "Greeting")
    if not Greeting.objects.filter(mensagem="Hello, world").exists():
        Greeting.objects.create(mensagem="Hello, world")


def unseed(apps, schema_editor):
    Greeting = apps.get_model("hello", "Greeting")
    Greeting.objects.filter(mensagem="Hello, world").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("hello", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
