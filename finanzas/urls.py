from django.urls import path
from . import views

urlpatterns = [
#    path('ingresos/', views.ingresos_mensuales, name='Ingreso-mensual'),
    path('gastos/', views.gastos_mensuales, name='gastos_mensuales'),
    path('caja_ahorro/', views.caja_Ahorro, name='caja_ahorro')
]