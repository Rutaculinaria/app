from django.db import models
from django.contrib.auth.models import User
import random
import string


class Plato(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=0)
    imagen = models.ImageField(upload_to='platos/', null=True, blank=True)
    
    def __str__(self):
        return self.nombre
    
class Pedido(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('aceptado', 'Aceptado'),
        ('rechazado', 'Rechazado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    platos = models.ManyToManyField(Plato, through='PedidoPlato')
    total = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    motivo_rechazo = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Pedido #{self.id} de {self.cliente.username} - Estado: {self.estado}"

class PedidoPlato(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.cantidad} x {self.plato.nombre} en Pedido #{self.pedido.id}"

class Orden(models.Model):
    cliente = models.ForeignKey(User, on_delete=models.CASCADE)
    plato = models.ForeignKey(Plato, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_retiro = models.DateField()
    hora_retiro = models.TimeField()
    precio_total = models.DecimalField(max_digits=10, decimal_places=0)
    confirmado = models.BooleanField(default=False)
    ESTADOS = [
        ('PENDIENTE', 'Pendiente'),
        ('CONFIRMADO', 'Confirmado'),
        ('FINALIZADO', 'Finalizado'),
        ('RECHAZADO', 'Rechazado')
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='PENDIENTE')
    motivo_rechazo = models.TextField(null=True, blank=True)
    codigo_autenticacion = models.CharField(max_length=8, null=True, blank=True)

    def calcular_precio_total(self):
        return self.cantidad * self.item.precio

    def __str__(self):
        return f"Orden de {self.cliente.username} - {self.plato.nombre}"
    
    def generar_codigo(self):
        self.codigo_autenticacion = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
