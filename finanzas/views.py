from django.shortcuts import render, redirect
from . import forms
from . import models
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
    saldo = saldo.disponible
    return render(request, 'dashboard/home.html', {'saldo': saldo})

@login_required
def ingresos_mensuales(request):
    ingresosMensuales = models.IngresoMensual.objects.filter(usuario=request.user).order_by('-fecha')[:10]

    if request.method == 'POST':
        form = forms.IngresoMensualForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.usuario = request.user
            ingreso.save()

            saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
            saldo.sumar_ingresos(ingreso.monto)
            saldo.save()
    else:
        form = forms.IngresoMensualForm()
        
    return render(request, 'Ingresar_datos/ingresos_mensuales.html', {'form': form, 'ingresos': ingresosMensuales})

            
 




