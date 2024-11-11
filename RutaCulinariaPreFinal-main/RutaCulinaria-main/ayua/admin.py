from django.contrib import admin
from .models import Plato, Pedido

# Register your models here.
@admin.register(Plato)
class PlatoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'precio')
    search_fields = ('nombre',)

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('estado',)
    list_filter = ('estado',)