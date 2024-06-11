from django.urls import path
from . import views

app_name = 'elama'

urlpatterns = [
    path('individual/nuevo/<int:autoevaluacion_id>/', views.nuevo_individual, name='nuevo_individual'),
    path(
        'individual/nuevo/<int:autoevaluacion_id>/<int:estrategia_id>/',
        views.nuevo_individual_principios, name='nuevo_individual_principios'
    ),
    path(
        'individual/nuevo/<int:autoevaluacion_id>/<int:estrategia_id>/<int:principio_codigo>/<int:descriptor_codigo>/',
        views.nuevo_individual_descriptor, name='nuevo_individual_descriptor'
    )
]
