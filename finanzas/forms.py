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

class IngresoCajaAhorroForm(forms.ModelForm):
    class Meta:
        model = models.IngresoAhorro
        fields = ['monto']
        widgets = {
            'monto' : forms.NumberInput(attrs={'class':'form-control'})
        }
        def clean_monto(self):
            monto = self.cleaned_data['total']
            if monto <= 0:
                raise forms.ValidationError("El monto debe ser mayor que 0")
            
            if self.user:
                saldoUsuario = models.SaldoUsuario.objects.filter(user=self.user).first()
                if not saldoUsuario or monto > saldoUsuario:
                    raise forms.ValidationError("No podes ingresar mas saldo del que tenes!")
            return monto