from django import forms
from . import models

class IngresoMensualForm(forms.ModelForm):
    class Meta:
        model = models.IngresoMensual
        fields = ['monto']
        widgets = {
            'monto' : forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'monto': 'Monto a ingresar(ARS)'
        }