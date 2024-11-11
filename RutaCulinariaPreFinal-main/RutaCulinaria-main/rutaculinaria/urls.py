"""
URL configuration for rutaculinaria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth.views import LogoutView
from ayua import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.mostrar_inicio, name='pagina_principal'),
    path('login_cliente/', views.login_cliente, name='login_cliente'),
    path('login_admin/', views.login_admin, name='login_admin'),
    path('registro_cliente/', views.registro_cliente, name='registro_cliente'),
    path('perfil_cliente/', views.perfil_cliente, name='perfil_cliente'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('orden/<int:plato_id>/', views.orden_actual, name='orden_actual'),
    path('ordenes/', views.todas_ordenes, name='ordenes'),
    path('carrito/', views.carrito_view, name='carrito'),
    path('orden/<int:plato_id>/editar/<int:pedido_id>/', views.orden_actual, name='editar_pedido'),
    path('orden/<int:pedido_id>/eliminar/', views.eliminar_pedido, name='eliminar_pedido'),
    path('confirmar_pedido/<int:pedido_id>/', views.confirmar_pedido, name='confirmar_pedido'),
    path('finalizar/<int:pedido_id>/', views.finalizar_pedido, name='finalizar_pedido'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('orden/<int:item_id>/', views.orden_actual, name='orden_actual'),
    path('ordenes/aceptar/<int:pedido_id>/', views.aceptar_pedido, name='aceptar_pedido'),
    path('ordenes/rechazar/<int:pedido_id>/', views.rechazar_pedido, name='rechazar_pedido'),
    path('menu_admin/', views.menu_admin, name='menu_admin'),
    path('menu_admin/<int:plato_id>/', views.menu_admin, name='editar_plato'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
