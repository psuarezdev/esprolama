from django.db import models

class Entidad(models.Model):
    class Meta:
        verbose_name_plural = "Entidades"

    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre