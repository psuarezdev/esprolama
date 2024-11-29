from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .models import Estrategia, Descriptor, Volcado, Autoevaluacion
from .services import IndividualService
from .forms import VolcadoForm

# FIXME: Todo el código ha sido creado dando por hecho que la autoevaluación ya ha sido creada previamente,
# FIXME: ya que se supone que el usuario al hacer clic en el botón para realizar la autoevaluación esta será creada


def nuevo_individual(request: HttpRequest, autoevaluacion_id: int):
    autoevaluacion = get_object_or_404(Autoevaluacion, pk=autoevaluacion_id)
    estrategias = Estrategia.objects.all()
    volcados = Volcado.objects.filter(autoevaluacion_id=autoevaluacion.id)

    return render(request, 'elama/nuevo_individual.html', {
        'autoevaluacion': autoevaluacion,
        'estrategias': estrategias,
        'volcados': volcados,
    })


def nuevo_individual_descriptor(request: HttpRequest, autoevaluacion_id: int, descriptor_id: int):
    autoevaluacion = get_object_or_404(Autoevaluacion, pk=autoevaluacion_id)
    descriptor = get_object_or_404(Descriptor, pk=descriptor_id)

    # FIXME: He creado un servicio para separar la lógica de la vista (paginación, creación de volcados, etc.),
    # FIXME: pero se podría incluir todo en la vista si se prefiere (aunque yo no lo recomendaría)
    paginacion = IndividualService.paginacion(descriptor=descriptor, autoevaluacion=autoevaluacion)

    if request.method == 'POST':
        guardar = 'guardar' in request.POST

        IndividualService.crear_volcado(
            data=request.POST, autoevaluacion=autoevaluacion,
            descriptor=paginacion['anterior_descriptor'] if not guardar else descriptor,
        )

        if guardar:
            # TODO: En este punto se deberían hacer las modificaciones necesarias para que el volcado no sea editable
            return redirect('elama:nuevo_individual', autoevaluacion_id=autoevaluacion.id)

    volcado = Volcado.objects.filter(
        autoevaluacion_id=autoevaluacion.id,
        descriptor_id=descriptor.id,
    ).first()

    # Si existe un volcado, se carga el formulario con los datos del volcado para poder editar
    if volcado is not None:
        form = VolcadoForm(instance=volcado)
    else:
        form = VolcadoForm()

    codigo_principio = ''

    if '.' in descriptor.principio.titulo:
        descriptor.principio.titulo.split('.')[0]

    return render(request, 'elama/nuevo_individual_descriptor.html', {
        'autoevaluacion': autoevaluacion,
        'descriptor': descriptor,
        'form': form,
        'codigo_principio': codigo_principio,
        **paginacion,
    })
