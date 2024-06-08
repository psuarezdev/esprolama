from django.urls import path
from . import views

urlpatterns = [
    path('individual/new/', views.new_individual, name='new_individual'),
    path('individual/new/<int:strategy_id>/', views.new_individual_principles, name='new_individual_principles'),
    path(
        'individual/new/<int:strategy_id>/<int:principle_id>/<int:descriptor_id>/',
        views.new_individual_descriptor,
        name='new_individual_descriptor'
    ),
]
