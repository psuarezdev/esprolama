from django import forms
from ..models import Volcado


class VolcadoForm(forms.ModelForm):
    class Meta:
        model = Volcado
        fields = ['respuesta']
        RESPUESTA_CHOICES = (
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
        )

        widgets = {'respuesta': forms.RadioSelect(choices=RESPUESTA_CHOICES)}
