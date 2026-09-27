from django.db import models


class Item(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-criado_em"]

    def __str__(self) -> str:
        return self.titulo
