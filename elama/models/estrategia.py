from django.db import models


class Estrategia(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo