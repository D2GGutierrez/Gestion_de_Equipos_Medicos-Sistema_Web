from django.urls import path
from .views import clientes, equipos, productos, reportes, suministros, tickets, usuarios

urlpatterns = [
    # Productos
    path('', productos.lista_productos, name='lista_productos'),
    path('productos/', productos.lista_productos),
    path('productos/nuevo/', productos.crear_producto, name='crear_producto'),
    path('productos/<int:pk>/editar/', productos.editar_producto, name='editar_producto'),
    path('productos/<int:pk>/eliminar/', productos.eliminar_producto, name='eliminar_producto'),

    # Productos con Proveedores (N:M) y CRUD de Suministro
    path('productos/proveedores/', productos.productos_proveedores, name='productos_proveedores'),
    path('productos/<int:producto_pk>/suministros/nuevo/', suministros.crear_suministro, name='crear_suministro'),
    path('suministros/<int:pk>/editar/', suministros.editar_suministro, name='editar_suministro'),
    path('suministros/<int:pk>/eliminar/', suministros.eliminar_suministro, name='eliminar_suministro'),

    # Categorías (acceso inverso)
    path('categorias/<int:pk>/', productos.detalle_categoria, name='detalle_categoria'),

    # Clientes
    path('clientes/', clientes.lista_clientes, name='lista_clientes'),
    path('clientes/<int:pk>/editar/', clientes.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/eliminar/', clientes.eliminar_cliente, name='eliminar_cliente'),

    # Usuarios
    path('usuarios/', usuarios.lista_usuarios, name='lista_usuarios'),
    path('usuarios/<int:pk>/editar/', usuarios.editar_usuario, name='editar_usuario'),
    path('usuarios/<int:pk>/eliminar/', usuarios.eliminar_usuario, name='eliminar_usuario'),

    # Equipos Instalados (RF-04)
    path('equipos/', equipos.lista_equipos, name='lista_equipos'),
    path('equipos/<int:pk>/editar/', equipos.editar_equipo, name='editar_equipo'),
    path('equipos/<int:pk>/eliminar/', equipos.eliminar_equipo, name='eliminar_equipo'),
    path('equipos/instalar/', equipos.registrar_instalacion, name='registrar_instalacion'),

    # Tickets de Soporte (RF-05)
    path('tickets/', tickets.lista_tickets, name='lista_tickets'),
    path('tickets/<int:pk>/editar/', tickets.editar_ticket, name='editar_ticket'),
    path('tickets/<int:pk>/eliminar/', tickets.eliminar_ticket, name='eliminar_ticket'),

    # Reporte (aggregate / annotate)
    path('reporte/', reportes.reporte, name='reporte'),
    path('reportes/postventa/', reportes.reporte_postventa, name='reporte_postventa'),

    # API REST (Django REST Framework)
    path('api/categorias/', productos.CategoriaListCreateView.as_view(), name='api_categorias'),
    path('api/categorias/<int:pk>/', productos.CategoriaDetailView.as_view(), name='api_categoria_detalle'),
]
