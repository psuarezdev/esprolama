from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from .models import Estrategia, Principio, Descriptor, Volcado, Autoevaluacion
from .services.individual_service import IndividualService
from .forms import volcado_form


def nuevo_individual(request: HttpRequest, autoevaluacion_id: int):
    estrategias = Estrategia.objects.all()
    return render(request, 'elama/nuevo_individual.html', {
        'autoevaluacion_id': autoevaluacion_id,
        'estrategias': estrategias
    })


def nuevo_individual_principios(request: HttpRequest, autoevaluacion_id: int, estrategia_id: int):
    principios = Principio.objects.filter(estrategia_id=estrategia_id)
    return render(request, 'elama/nuevo_individual_principios.html', {
        'autoevaluacion_id': autoevaluacion_id,
        'estrategia_id': estrategia_id,
        'principios': principios,
    })


def nuevo_individual_descriptor(
        request: HttpRequest, autoevaluacion_id: int, estrategia_id: int, principio_codigo: int, descriptor_codigo: int
):
    paginacion = IndividualService.descriptor_paginacion(
        estrategia_id=estrategia_id, principio_codigo=principio_codigo, descriptor_codigo=descriptor_codigo
    )

    ultimo_principio = Principio.objects.filter(estrategia_id=estrategia_id).last()
    ultimo_descriptor = Descriptor.objects.filter(
        principio__estrategia_id=estrategia_id, principio_id=ultimo_principio.id
    ).last()

    # TODO: Mover esto al servicio -> IndividualService
    if request.method == 'POST':
        IndividualService.crear_volcado(
            data=request.POST, autoevaluacion_id=autoevaluacion_id, estrategia_id=estrategia_id, paginacion=paginacion
        )

        if (ultimo_principio.codigo == paginacion['principio_anterior']
                and ultimo_descriptor.codigo == paginacion['descriptor_anterior']):
            return redirect('elama:nuevo_individual', autoevaluacion_id)

    descriptor = Descriptor.objects.filter(
        principio__estrategia_id=estrategia_id,
        principio__codigo=principio_codigo,
        codigo=descriptor_codigo
    ).first()

    volcado = Volcado.objects.filter(
        autoevaluacion_id=autoevaluacion_id,
        descriptor__principio__estrategia_id=estrategia_id,
        descriptor__principio__codigo=principio_codigo,
        descriptor__codigo=descriptor_codigo,
    ).first()

    if volcado is not None:
        form = volcado_form.VolcadoForm(instance=volcado)
    else:
        form = volcado_form.VolcadoForm()

    return render(request, 'elama/nuevo_individual_descriptor.html', {
        'autoevaluacion_id': autoevaluacion_id,
        'descriptor': descriptor,
        'form': form,
        'es_ultimo': (ultimo_principio.codigo < paginacion['principio_siguiente']
                        and ultimo_descriptor.codigo > paginacion['descriptor_siguiente']),
        **paginacion,
    })
