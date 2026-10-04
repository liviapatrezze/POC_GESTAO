from django.db import models


class Greeting(models.Model):
    mensagem = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.mensagem
