from . import models

def saldo_usuario(request):
    if request.user.is_authenticated:
        saldo = models.SaldoUsuario.objects.filter(user=request.user).first()
        return {'saldo_usuario': saldo}
    return {}