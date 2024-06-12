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


def nuevo_individual_descriptor(request: HttpRequest, autoevaluacion_id: int, descriptor_id: int):
    descriptor = get_object_or_404(Descriptor, pk=descriptor_id)

    es_primero = Principio.objects.filter(
        estrategia_id=descriptor.principio.estrategia.id
    ).first().descriptor_set.first().id == descriptor.id
    es_ultimo = Principio.objects.filter(
        estrategia_id=descriptor.principio.estrategia.id
    ).last().descriptor_set.last().id == descriptor.id

    # TODO: terminar paginación -> anterior_descriptor =
    siguiente_descriptor = Descriptor.objects.filter(
        principio__estrategia_id=descriptor.principio.estrategia.id,
        principio_id=descriptor.principio.id,
        id__gt=descriptor.id
    ).first()

    if es_ultimo:
        siguiente_descriptor = descriptor

    if not es_ultimo and siguiente_descriptor is None:
        siguiente_principio = Principio.objects.filter(
            estrategia_id=descriptor.principio.estrategia.id,
            id__gt=descriptor.principio.id,
        ).first()

        if siguiente_principio is None:
            return redirect('elama:nuevo_individual', autoevaluacion_id)

        siguiente_descriptor = Descriptor.objects.filter(
            principio__estrategia_id=descriptor.principio.estrategia.id,
            principio_id=siguiente_principio.id,
        ).first()

    volcado = Volcado.objects.filter(
        autoevaluacion_id=autoevaluacion_id,
        descriptor_id=descriptor.id,
    ).first()

    if volcado is not None:
        form = volcado_form.VolcadoForm(instance=volcado)
    else:
        form = volcado_form.VolcadoForm()

    return render(request, 'elama/nuevo_individual_descriptor.html', {
        'autoevaluacion_id': autoevaluacion_id,
        'codigo_principio': descriptor.principio.titulo.split('.')[0],
        'form': form,
        'descriptor': descriptor,
        'siguiente_descriptor': siguiente_descriptor,
        'es_primero': es_primero,
        'es_ultimo': es_ultimo,
    })
