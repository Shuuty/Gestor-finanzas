from django.contrib import admin
from .models import CategoriaGastos

@admin.register(CategoriaGastos)
class CategoriaGastosAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'user', 'es_global']
    list_filter = ['es_global']