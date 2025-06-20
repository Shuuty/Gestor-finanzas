from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SaldoUsuario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    disponible = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def sumar_ingresos(self, saldo):
        self.disponible += saldo

    def restar_gastos(self, saldo):
        self.disponible -= saldo
    
    def transferir_a_ahorro(self, saldo):
        if saldo <= self.disponible:
            self.disponible -= saldo
            self.save()
            ahorro, _ = CajadeAhorros.objects.get_or_create(user=self.user)
            ahorro.total += saldo
            ahorro.save()
            IngresoAhorro.objects.create(user=self.user, monto=saldo)

    def sacar_de_ahorro(self, saldo):
        self.disponible += saldo
        self.save()
        ahorro, _ = CajadeAhorros.objects.get_or_create(user=self.user)
        ahorro.total -= saldo
        ahorro.save()
        RetiroAhorro.objects.create(user=self.user, monto=saldo)



class IngresoMensual(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class CategoriaGastos(models.Model):
    nombre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    es_global = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
    
class Gastos(models.Model):
    nombre = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    categoria = models.ForeignKey(CategoriaGastos, on_delete=models.SET_NULL, null=True)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    nota = models.TextField(blank=True, null=True)
    es_recurrente = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.categoria} - ${self.monto}"


class CajadeAhorros(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    


class IngresoAhorro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class RetiroAhorro(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2)

class ResumenMensual(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()

    dinero_ingresado = models.ManyToManyField(IngresoMensual)
    movimientosGastos = models.ManyToManyField(Gastos)
    movimientosAhorro = models.ManyToManyField(IngresoAhorro)





    

    