from django.urls import path
from . import views

urlpatterns = [
    path('ingresos/', views.ingresos_mensuales, name='Ingreso-mensual'),
    path('', views.home, name='home')
    
]