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
    # TODO: Arreglar finalizar
    # TODO: preguntar a Juan Pablo si el uso del formulario en el html es correcto
    descriptor = get_object_or_404(
        Descriptor,
        principio__estrategia_id=estrategia_id,
        principio__codigo=principio_codigo,
        codigo=descriptor_codigo
    )

    paginacion = IndividualService.descriptor_paginacion(estrategia_id, principio_codigo, descriptor_codigo)
    ultimo_principio = Principio.objects.filter(estrategia_id=estrategia_id).last()
    ultimo_descriptor = Descriptor.objects.filter(
        principio__estrategia_id=estrategia_id, principio_id=ultimo_principio.id
    ).last()
    es_ultimo = descriptor.principio.codigo == ultimo_principio.codigo and descriptor.codigo == ultimo_descriptor.codigo

    if request.method == 'POST':
        volcado = Volcado.objects.filter(
            autoevaluacion_id=autoevaluacion_id,
            descriptor__principio__estrategia_id=estrategia_id,
            descriptor__principio__codigo=paginacion['principio_anterior'],
            descriptor__codigo=paginacion['descriptor_anterior'],
        ).first()

        if volcado is not None:
            form = volcado_form.VolcadoForm(instance=volcado, data=request.POST)
            if form.is_valid():
                form.save()
        else:
            form = volcado_form.VolcadoForm(data=request.POST)
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
        'es_ultimo': es_ultimo,
        **paginacion,
    })
