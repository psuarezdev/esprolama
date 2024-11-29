from django.db import models
from . import Principio


class Descriptor(models.Model):
    class Meta:
        verbose_name_plural = "Descriptores"

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    principio = models.ForeignKey(Principio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Estrategia {self.principio.estrategia.id} - Principio {self.principio.id} - Descriptor {self.id}'