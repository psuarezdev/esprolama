from django.urls import path
from . import views

app_name = 'elama'

urlpatterns = [
    path('individual/nuevo/<int:autoevaluacion_id>/', views.nuevo_individual, name='nuevo_individual'),
    path(
        'individual/nuevo/<int:autoevaluacion_id>/<int:descriptor_id>/',
        views.nuevo_individual_descriptor, name='nuevo_individual_descriptor'
    )
]
