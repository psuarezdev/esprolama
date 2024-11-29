from django.db import models
from . import Estrategia


class Principio(models.Model):
    titulo = models.CharField(max_length=200)
    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE)

    def __str__(self):
        return f'Estrategia {self.estrategia.id} - {self.titulo}'