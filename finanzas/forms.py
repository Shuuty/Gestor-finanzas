from django import forms
from . import models

class IngresoMensualForm(forms.ModelForm):
    class Meta:
        model = models.IngresoMensual
        fields = ['fecha', 'monto']
        widgets = {
            'fecha' : forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'monto' : forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
        labels = {
            'fecha': 'Fecha del Ingreso',
            'monto': 'Monto a ingresar(ARS)'
        }