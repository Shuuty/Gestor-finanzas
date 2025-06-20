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

@login_required
def gastos_mensuales(request):
    gastos = models.Gastos.objects.filter(user=request.user).order_by('-fecha')[:10]
    if request.method == 'POST':
        form = forms.GastosForm(request.POST)
        if form.is_valid():
            gasto = form.save(commit=False)
            gasto.user = request.user
            gasto.save()

            saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
            saldo.restar_gastos(gasto.monto)
            saldo.save()
    else:
        form = forms.GastosForm()

    return render(request, 'Ingresar_datos/gastos_mensuales.html', {'form': form, 'gastos': gastos})

@login_required
def ingresar_saldo_cajaAhorro(request):
    cajaAhorro, _ = models.CajadeAhorros.objects.get_or_create(user=request.user)
    cajaAhorroHistorial = models.IngresoAhorro.objects.filter(user=request.user).order_by('-id')[:10]
    if request.method == 'POST':
        form = forms.IngresoCajaAhorroForm(request.POST)
        if form.is_valid():
            ahorro = form.cleaned_data['monto']
            saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
            saldo.transferir_a_ahorro(ahorro)
            saldo.save()
    else:
        form = forms.IngresoCajaAhorroForm()

    return render(request, 'Ingresar_datos/caja_ahorro.html', {'form': form, 'cajaAhorro': cajaAhorro, 'historial': cajaAhorroHistorial})

            
 




