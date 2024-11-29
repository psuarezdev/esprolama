from django.db import models


class Autoevaluacion(models.Model):
    class Meta:
        verbose_name_plural = "Autoevaluaciones"

    # TODO: Añadir el identificador del evaluador
    # tipo_trabajo = models.CharField(max_length=200)
    # n_integrantes = models.IntegerField()
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return f'Autoevaluación {self.id}'