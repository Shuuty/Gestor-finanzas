from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('ingresos/', views.ingresos_mensuales, name='Ingreso-mensual'),
    path('gastos/', views.gastos_mensuales, name='gastos_mensuales')
]