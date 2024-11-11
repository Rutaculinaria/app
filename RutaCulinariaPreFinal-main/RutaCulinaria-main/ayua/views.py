from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Pedido, Plato, Orden
from .forms import ClienteRegistroForm, OrdenForm, PlatoForm
from datetime import datetime, date, time
from decimal import Decimal
import random
import string

def menu(request):
    items = Plato.objects.all()
    return render(request, 'inicio.html', {'menu_items': items})

@login_required
def orden_actual(request, plato_id, pedido_id=None):
    plato = get_object_or_404(Plato, id=plato_id)
    
    if pedido_id:
        orden = get_object_or_404(Orden, id=pedido_id, cliente=request.user)
    else:
        orden = Orden(cliente=request.user, plato=plato)
    
    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=orden)
        if form.is_valid():
            orden = form.save(commit=False)
            orden.plato = plato
            orden.precio_total = plato.precio * orden.cantidad

            if 'guardar_carrito' in request.POST:
                orden.confirmado = False
                messages.success(request, "Pedido guardado en el carrito.")
                orden.save()
                return redirect('carrito')
            elif 'confirmar_pedido' in request.POST:
                orden.confirmado = True
                orden.estado = 'pendiente'
                messages.success(request, "Pedido confirmado.")
                orden.save()
                return redirect('perfil_cliente')
    else:
        form = OrdenForm(instance=orden)

    return render(request, 'orden_actual.html', {'form': form, 'plato': plato, 'orden': orden})

@login_required
def carrito_view(request):
    pedidos = Orden.objects.filter(cliente=request.user, confirmado=False).order_by('id')
    
    total = sum(pedido.precio_total for pedido in pedidos)
    
    return render(request, 'carrito.html', {
        'pedidos': pedidos,
        'total': total
    })

def confirmar_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    if request.method == 'POST':
        pedido.confirmado = True
        pedido.estado = 'pendiente'
        pedido.save()
        return redirect('perfil_cliente')
    return redirect('orden_actual')

@login_required
def guardar_pedido(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 1))
        fecha_retiro = request.POST.get('fecha_retiro')
        hora_retiro = request.POST.get('hora_retiro')
        
        pedido = Orden.objects.create(
            cliente=request.user,
            plato=plato,
            cantidad=cantidad,
            fecha_retiro=fecha_retiro,
            hora_retiro=hora_retiro,
            precio_total=plato.precio * cantidad,
            confirmado=False
        )
        pedido.save()
        return redirect('carrito')


@login_required
def eliminar_pedido(request, pedido_id):
    pedido = get_object_or_404(Orden, id=pedido_id)
    pedido.delete()
    return redirect('carrito')

def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(Orden, id=pedido_id)

    if request.method == 'POST':
        form = OrdenForm(request.POST, instance=pedido)
        if form.is_valid():
            pedido = form.save(commit=False)
            pedido.precio_total = pedido.cantidad * pedido.plato.precio
            pedido.save()
            return redirect('carrito')
    else:
        form = OrdenForm(instance=pedido)

    return render(request, 'orden_actual.html', {'form': form, 'plato': pedido.plato, 'pedido': pedido})

@login_required
def finalizar_pedido(request, pedido_id):
    pedido = get_object_or_404(Orden, id=pedido_id, cliente=request.user)
    pedido.confirmado = True
    pedido.estado = 'pendiente'
    pedido.save()
    return redirect('perfil_cliente')

def admin_required(login_url='login_admin'):
    return user_passes_test(lambda u: u.is_staff, login_url=login_url)

def mostrar_inicio(request):
    menu_items = Plato.objects.all() 
    return render(request, 'inicio.html', {'menu_items': menu_items})

def login_cliente(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        usuario = authenticate(request, username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('pagina_principal')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
    return render(request, 'login_cliente.html')

def login_admin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('ordenes')
    return render(request, 'login_admin.html')

def registro_cliente(request):
    if request.method == 'POST':
        form = ClienteRegistroForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            telefono = form.cleaned_data.get('telefono')

            user = User.objects.create_user(username=username, password=password)
            user.save()

            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('pagina_principal')
    else:
        form = ClienteRegistroForm()
    return render(request, 'registro_cliente.html', {'form': form})

def cerrar_sesion(request):
    logout(request)
    return redirect('pagina_principal')

@login_required
def perfil_cliente(request):
    pedidos = Orden.objects.filter(cliente=request.user)
    return render(request, 'perfil_cliente.html', {'pedidos': pedidos})

@login_required
@admin_required()
def menu_admin(request, plato_id=None):
    platos = Plato.objects.all()
    plato = None

    if plato_id:
        plato = get_object_or_404(Plato, id=plato_id)

    if request.method == "POST":
        if plato:
            form = PlatoForm(request.POST, request.FILES, instance=plato)
        else:
            form = PlatoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('menu_admin')
    else:
        form = PlatoForm(instance=plato)

    return render(request, 'menu_admin.html', {'platos': platos, 'form': form, 'plato': plato})

@admin_required()
def todas_ordenes(request):
    pedidos_pendientes = Orden.objects.filter(estado='pendiente', confirmado=True)
    pedidos_aceptados = Orden.objects.filter(estado='aceptado')
    pedidos_rechazados = Orden.objects.filter(estado='rechazado')

    context = {
        'pedidos_pendientes': pedidos_pendientes,
        'pedidos_aceptados': pedidos_aceptados,
        'pedidos_rechazados': pedidos_rechazados,
    }
    return render(request, 'ordenes.html', context)

@admin_required()
def rechazar_pedido(request, pedido_id):
    pedido = get_object_or_404(Orden, id=pedido_id)
    if request.method == 'POST':
        motivo = request.POST.get('motivo_rechazo')
        if motivo:
            pedido.estado = 'rechazado'
            pedido.motivo_rechazo = motivo
            pedido.save()
            messages.error(request, "Pedido rechazado exitosamente.")
    return redirect('ordenes')

@admin_required()
def aceptar_pedido(request, pedido_id):
    pedido = get_object_or_404(Orden, id=pedido_id)
    if request.method == 'POST':
        codigo_autenticacion = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        pedido.estado = 'aceptado'
        pedido.codigo_autenticacion = codigo_autenticacion
        pedido.save()
        return redirect('todas_ordenes')

@login_required
@admin_required()
def editar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    if request.method == "POST":
        plato.nombre = request.POST.get('nombre')
        plato.precio = request.POST.get('precio')
        plato.save()
        return redirect('ordenes')
    return render(request, 'menu_admin.html', {'plato': plato})

@login_required
@admin_required()
def eliminar_plato(request, plato_id):
    plato = get_object_or_404(Plato, id=plato_id)
    plato.delete()
    return redirect('menu_admin')