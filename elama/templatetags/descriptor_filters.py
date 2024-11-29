from django.db.models.query import QuerySet
from elama.models import Descriptor, Volcado
from django import template


register = template.Library()

@register.filter(name='descriptor_in_volcado')
def descriptor_in_volcado(descriptor: Descriptor, volcados: QuerySet[Volcado]):
    return volcados.filter(descriptor_id=descriptor.id).first()
