from ..models import Principio, Descriptor, Volcado
from ..forms import volcado_form


class IndividualService:
    @staticmethod
    def descriptor_paginacion(estrategia_id: int, principio_codigo: int, descriptor_codigo: int):
        principio_anterior = principio_codigo
        principio_siguiente = principio_codigo
        descriptor_anterior = descriptor_codigo - 1
        descriptor_siguiente = descriptor_codigo + 1

        if descriptor_anterior == 0:
            ultimo_descriptor = Descriptor.objects.filter(
                principio__estrategia_id=estrategia_id, principio__codigo__lt=principio_codigo
            ).last()

            if ultimo_descriptor is not None:
                principio_anterior = ultimo_descriptor.principio.codigo
                descriptor_anterior = ultimo_descriptor.codigo

        ultimo_descriptor_principio = Descriptor.objects.filter(
            principio__estrategia_id=estrategia_id, principio__codigo=principio_codigo
        ).last()
        if ultimo_descriptor_principio is None or descriptor_siguiente > ultimo_descriptor_principio.codigo:
            principio_siguiente = Principio.objects.filter(
                estrategia_id=estrategia_id, codigo__gt=principio_codigo
            ).first()

            if principio_siguiente is not None:
                principio_siguiente = principio_siguiente.codigo
                primer_descriptor = Descriptor.objects.filter(
                    principio__estrategia_id=estrategia_id, principio__codigo=principio_codigo
                ).first()
                descriptor_siguiente = primer_descriptor.codigo if principio_siguiente is not None else 1
            else:
                principio_siguiente = principio_codigo + 1
                descriptor_siguiente = 1

        return {
            'principio_anterior': principio_anterior,
            'principio_siguiente': principio_siguiente,
            'descriptor_anterior': descriptor_anterior,
            'descriptor_siguiente': descriptor_siguiente,
        }

    @staticmethod
    def crear_volcado(data, autoevaluacion_id: int, estrategia_id: int, paginacion: dict):
            volcado = Volcado.objects.filter(
                autoevaluacion_id=autoevaluacion_id,
                descriptor__principio__estrategia_id=estrategia_id,
                descriptor__principio__codigo=paginacion['principio_anterior'],
                descriptor__codigo=paginacion['descriptor_anterior'],
            ).first()

            if volcado is not None:
                form = volcado_form.VolcadoForm(instance=volcado, data=data)
                if form.is_valid():
                    form.save()
            else:
                form = volcado_form.VolcadoForm(data=data)
                if form.is_valid():
                    descriptor_anterior = Descriptor.objects.filter(
                        principio__estrategia_id=estrategia_id,
                        principio__codigo=paginacion['principio_anterior'],
                        codigo=paginacion['descriptor_anterior'],
                    ).first()

                    volcado = form.save(commit=False)
                    volcado.autoevaluacion_id = autoevaluacion_id
                    volcado.descriptor = descriptor_anterior
                    volcado.save()

