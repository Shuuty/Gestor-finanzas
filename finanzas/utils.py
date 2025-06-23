from django.utils import timezone
from datetime import date
from collections import defaultdict
from django.db.models import Sum
from .models import Gastos, Ingreso, IngresoAhorro, RetiroAhorro


def obtener_datos_dashboard(user):
    hoy = timezone.now().date()
    inicio_mes = date(hoy.year, hoy.month, 1)

    # Totales
    total_gastos = Gastos.objects.filter(user=user, fecha__gte=inicio_mes).aggregate(total=Sum('monto'))['total'] or 0
    total_ingresos = Ingreso.objects.filter(user=user, fecha__gte=inicio_mes).aggregate(total=Sum('monto'))['total'] or 0
    total_ahorro_mes = IngresoAhorro.objects.filter(user=user, fecha__gte=inicio_mes).aggregate(total=Sum('monto'))['total'] or 0
    total_retiros_mes = RetiroAhorro.objects.filter(user=user, fecha__gte=inicio_mes).aggregate(total=Sum('monto'))['total'] or 0


    # Porcentaje de ahorro
    porcentaje_ahorro = (total_ahorro_mes / total_ingresos * 100) if total_ingresos else 0

    # Porcentaje de gasto por categoría
    gastos = Gastos.objects.filter(user=user, fecha__gte=inicio_mes)
    porcentajes_por_categoria = defaultdict(float)
    for gasto in gastos:
        if total_ingresos > 0:
            porcentaje = (gasto.monto / total_ingresos) * 100
            porcentajes_por_categoria[gasto.categoria] += round(porcentaje, 2)

    # Alerta: gastos mayores a ingresos
    alerta = total_gastos > total_ingresos

    # Últimos movimientos
    ultimos_gastos = gastos.order_by('-fecha')[:5]
    ultimos_ingresos = Ingreso.objects.filter(user=user).order_by('-fecha')[:5]
    ultimos_movimientos_ahorro = list(IngresoAhorro.objects.filter(user=user).order_by('-fecha')[:3]) + \
                                 list(RetiroAhorro.objects.filter(user=user).order_by('-fecha')[:3])

    # Gasto promedio diario
    dia_del_mes = hoy.day
    gasto_promedio_diario = total_gastos / dia_del_mes if dia_del_mes > 0 else 0

    return {
        'total_gastos': round(total_gastos, 2),
        'total_ingresos': round(total_ingresos, 2),
        'porcentaje_ahorro': round(porcentaje_ahorro, 2),
        'porcentajes_por_categoria': dict(porcentajes_por_categoria),
        'alerta': alerta,
        'ultimos_gastos': ultimos_gastos,
        'ultimos_ingresos': ultimos_ingresos,
        'ultimos_movimientos_ahorro': ultimos_movimientos_ahorro,
        'gasto_promedio_diario': round(gasto_promedio_diario, 2),
    }