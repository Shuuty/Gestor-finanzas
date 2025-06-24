from django.shortcuts import render, redirect
from . import forms
from . import models
from . import utils
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def home(request):
    datos_home = utils.obtener_datos_dashboard(request.user)
    return render(request, 'dashboard/home.html', {'datos': datos_home})


@login_required
def ingresos_mensuales(request):
    ingresosMensuales = models.IngresoMensual.objects.filter(user=request.user).order_by('-fecha')[:10]

    if request.method == 'POST':
        form = forms.IngresoMensualForm(request.POST)
        if form.is_valid():
            ingreso = form.save(commit=False)
            ingreso.user = request.user
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
def caja_Ahorro(request):
    cajaAhorro, _ = models.CajadeAhorros.objects.get_or_create(user=request.user)
    cajaAhorroIngresos = models.IngresoAhorro.objects.filter(user=request.user).order_by('-id')[:10]
    cajaAhorroRetiros= models.RetiroAhorro.objects.filter(user=request.user).order_by('-id')[:10]

    if request.method == 'POST':
        form = forms.CajaAhorroForm(request.POST, user=request.user)
        if form.is_valid():
            ahorro = form.cleaned_data['monto']
            accion = form.cleaned_data['accion']

            if accion == 'ingreso':
                saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
                saldo.transferir_a_ahorro(ahorro)
                saldo.save()

            elif accion == 'retiro':
                saldo, _ = models.SaldoUsuario.objects.get_or_create(user=request.user)
                saldo.sacar_de_ahorro(ahorro)
                saldo.save()
            
            return redirect('caja_ahorro')

    else:
        form = forms.CajaAhorroForm()

    return render(request, 'Ingresar_datos/caja_ahorro.html', {'form': form, 'cajaAhorro': cajaAhorro, 'historial_ingresos': cajaAhorroIngresos, 'historial_retiros': cajaAhorroRetiros})



