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

class GastosForm(forms.ModelForm):
    class Meta:
        model = models.Gastos
        fields = ['nombre', 'categoria', 'monto', 'nota', 'es_recurrente']
        widgets = {
            'nombre' : forms.TextInput(attrs={'class': 'form-control', 'maxlenght': '50'}),
            'monto' : forms.NumberInput(attrs={'class': 'form-control'}),
            'nota' : forms.Textarea(attrs={'class':'form-control', 'rows':'2'}),
            'es_recurrente': forms.CheckboxInput(attrs={'class': 'form-control'})
        }