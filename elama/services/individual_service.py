from django.shortcuts import redirect
from django.http import QueryDict
from typing import Type
from ..models import Principio, Descriptor, Volcado, Autoevaluacion
from ..forms.volcado_form import VolcadoForm


class IndividualService:
    @staticmethod
    def paginacion(autoevaluacion: Autoevaluacion, descriptor: Descriptor):
        principios = Principio.objects.filter(estrategia_id=descriptor.principio.estrategia.id)

        # Obtener el primer y último descriptor para poder manejar el "Volver" y "Guardar" de la paginación
        primer_descriptor = principios.first().descriptor_set.first()
        ultimo_descriptor = principios.last().descriptor_set.last()

        # Obtener el siguiente descriptor y el anterior para poder manejar el "Siguiente" y "Anterior" de la paginación
        anterior_descriptor = Descriptor.objects.filter(
            principio__estrategia_id=descriptor.principio.estrategia.id,
            principio_id=descriptor.principio.id,
            id__lt=descriptor.id
        ).last()
        siguiente_descriptor = Descriptor.objects.filter(
            principio__estrategia_id=descriptor.principio.estrategia.id,
            principio_id=descriptor.principio.id,
            id__gt=descriptor.id
        ).first()

        # Si es el último descriptor, el siguiente descriptor será el mismo para evitar errores
        if ultimo_descriptor.id == descriptor.id:
            siguiente_descriptor = descriptor
        elif ultimo_descriptor.id != descriptor.id and siguiente_descriptor is None:
            # Si no es el último descriptor y no hay siguiente descriptor,
            # se debe buscar el primer descriptor del siguiente principio,
            # si no hay siguiente principio, se redirige a la vista de nuevo_individual (ultimo principio)
            siguiente_principio = Principio.objects.filter(
                estrategia_id=descriptor.principio.estrategia.id,
                id__gt=descriptor.principio.id,
            ).first()

            if siguiente_principio is None:
                return redirect('elama:nuevo_individual', autoevaluacion.id)

            siguiente_descriptor = siguiente_principio.descriptor_set.first()

        # Si no es el primer descriptor y no hay anterior descriptor,
        # se debe buscar el último descriptor del anterior principio,
        # si no hay anterior principio, se redirige a la vista de nuevo_individual (primer principio)
        if primer_descriptor.id != descriptor.id and anterior_descriptor is None:
            anterior_principio = Principio.objects.filter(
                estrategia_id=descriptor.principio.estrategia.id,
                id__lt=descriptor.principio.id,
            ).last()

            if anterior_principio is None:
                return redirect('elama:nuevo_individual', autoevaluacion.id)

            anterior_descriptor = anterior_principio.descriptor_set.last()

        return {
            'primer_descriptor': primer_descriptor,
            'ultimo_descriptor': ultimo_descriptor,
            'siguiente_descriptor': siguiente_descriptor,
            'anterior_descriptor': anterior_descriptor,
        }

    @staticmethod  # data = request.POST
    def crear_volcado(data: Type[QueryDict], autoevaluacion: Autoevaluacion, descriptor: Descriptor):
        volcado = Volcado.objects.filter(autoevaluacion_id=autoevaluacion.id, descriptor_id=descriptor.id).first()

        if volcado is not None:
            form = VolcadoForm(instance=volcado, data=data)
            if form.is_valid():
                form.save()
        else:
            form = VolcadoForm(data=data)
            if form.is_valid():
                volcado = form.save(commit=False)
                volcado.autoevaluacion = autoevaluacion
                volcado.descriptor = descriptor
                volcado.save()
