from django.db import models
from . import Descriptor
from . import Autoevaluacion


class Volcado(models.Model):
    # TODO: Añadir el identificador del evaluador
    respuesta = models.IntegerField()
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    autoevaluacion = models.ForeignKey(Autoevaluacion, on_delete=models.CASCADE)
