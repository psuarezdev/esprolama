from django.db import models


class Entidad(models.Model):
    class Meta:
        verbose_name_plural = "Entidades"

    nombre = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre


class Programa(models.Model):
    titulo = models.CharField(max_length=200)
    entidad = models.ForeignKey(Entidad, on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo


class Estrategia(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class Principio(models.Model):
    titulo = models.CharField(max_length=200)
    estrategia = models.ForeignKey(Estrategia, on_delete=models.CASCADE)

    def __str__(self):
        return f'Estrategia {self.estrategia.id} - {self.titulo}'


class Descriptor(models.Model):
    class Meta:
        verbose_name_plural = "Descriptores"

    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    principio = models.ForeignKey(Principio, on_delete=models.CASCADE)

    def __str__(self):
        return f'Estrategia {self.principio.estrategia.id} - Principio {self.principio.id} - Descriptor {self.id}'


class Autoevaluacion(models.Model):
    class Meta:
        verbose_name_plural = "Autoevaluaciones"

    # TODO: Añadir el identificador del evaluador
    # tipo_trabajo = models.CharField(max_length=200)
    # n_integrantes = models.IntegerField()
    fecha_hora = models.DateTimeField()

    def __str__(self):
        return f'Autoevaluación {self.id}'


class Volcado(models.Model):
    # TODO: Añadir el identificador el evaluador
    respuesta = models.IntegerField()
    descriptor = models.ForeignKey(Descriptor, on_delete=models.CASCADE)
    autoevaluacion = models.ForeignKey(Autoevaluacion, on_delete=models.CASCADE)
