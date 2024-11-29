from django.db import models
from . import Entidad


class Programa(models.Model):
    titulo = models.CharField(max_length=200)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo