import calendar
from datetime import date

from django.contrib import messages
from django.db import IntegrityError, transaction
from django.db.models import Count, DecimalField, ExpressionWrapper, F, Q, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from .models import Producto, Cliente, Usuario, EquipoInstalado, TicketSoporte, Suministro, Proveedor, Categoria, FichaTecnica
from .forms import ProductoForm, ClienteForm, UsuarioForm, EquipoInstaladoForm, TicketSoporteForm, SuministroForm, RegistrarInstalacionForm


# Vista para Listar Productos (Optimizado con select_related para 1:1 y 1:N)
def lista_productos(request):
    productos = Producto.objects.select_related('categoria', 'ficha_tecnica').all().order_by('nombre')
    return render(request, 'inventario/lista_productos.html', {'productos': productos})


# Vista para Consultar Productos con Proveedores (Optimizado con prefetch_related para N:M con modelo intermedio)
def productos_proveedores(request):
    productos = Producto.objects.prefetch_related(
        'suministro_set__proveedor'
    ).order_by('nombre')

    return render(request, 'inventario/productos_proveedores.html', {'productos': productos})


# Vista para Crear un Producto (CREATE mediante ORM)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en SQLite usando Django ORM
            return redirect('lista_productos')  # Redirige al listado
    else:
        form = ProductoForm()

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': 'Registrar Nuevo Producto Médico', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Actualizar un Producto (UPDATE mediante ORM)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # UPDATE en SQLite usando Django ORM
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Producto: {producto}', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Eliminar un Producto (DELETE mediante ORM, con confirmacion previa)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()  # DELETE en SQLite usando Django ORM
        return redirect('lista_productos')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': producto, 'titulo_entidad': 'Producto', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Listar Clientes (RF: consulta de clientes registrados)
def lista_clientes(request):
    clientes = Cliente.objects.all().order_by('razon_social')

    estado = request.GET.get('estado')
    if estado == 'activos':
        clientes = clientes.filter(activo=True)
    elif estado == 'inactivos':
        clientes = clientes.filter(activo=False)

    return render(request, 'inventario/lista_clientes.html', {
        'clientes': clientes,
        'estado_seleccionado': estado,
    })


# Vista para Actualizar un Cliente (UPDATE mediante ORM)
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('lista_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Cliente: {cliente}', 'url_cancelar': reverse('lista_clientes'),
    })


# Vista para Eliminar un Cliente (DELETE mediante ORM, con confirmacion previa)
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        return redirect('lista_clientes')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': cliente, 'titulo_entidad': 'Cliente', 'url_cancelar': reverse('lista_clientes'),
    })


# Vista para Listar Usuarios del sistema
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('nombre_completo')

    rol = request.GET.get('rol')
    if rol:
        usuarios = usuarios.filter(rol=rol)

    return render(request, 'inventario/lista_usuarios.html', {
        'usuarios': usuarios,
        'roles': Usuario.ROLES,
        'rol_seleccionado': rol,
    })


# Vista para Actualizar un Usuario (UPDATE mediante ORM)
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Usuario: {usuario}', 'url_cancelar': reverse('lista_usuarios'),
    })


# Vista para Eliminar un Usuario (DELETE mediante ORM, con confirmacion previa)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': usuario, 'titulo_entidad': 'Usuario', 'url_cancelar': reverse('lista_usuarios'),
    })


# Vista para Listar Equipos Instalados (RF-04)
# Filtros soportados: cliente, estado de garantia y rango de fechas de instalacion
def lista_equipos(request):
    equipos = EquipoInstalado.objects.select_related('producto', 'cliente').all().order_by('-fecha_instalacion')

    cliente_id = request.GET.get('cliente')
    garantia = request.GET.get('garantia')
    desde = request.GET.get('desde')
    hasta = request.GET.get('hasta')

    if cliente_id:
        equipos = equipos.filter(cliente_id=cliente_id)

    hoy = timezone.now().date()
    if garantia == 'vigente':
        equipos = equipos.filter(fin_garantia__gte=hoy)
    elif garantia == 'vencida':
        equipos = equipos.filter(fin_garantia__lt=hoy)

    if desde:
        equipos = equipos.filter(fecha_instalacion__gte=desde)
    if hasta:
        equipos = equipos.filter(fecha_instalacion__lte=hasta)

    return render(request, 'inventario/lista_equipos.html', {
        'equipos': equipos,
        'clientes': Cliente.objects.all().order_by('razon_social'),
        'filtros': {
            'cliente': cliente_id,
            'garantia': garantia,
            'desde': desde or '',
            'hasta': hasta or '',
        },
    })


# Vista para Actualizar un Equipo Instalado (UPDATE mediante ORM)
def editar_equipo(request, pk):
    equipo = get_object_or_404(EquipoInstalado, pk=pk)
    if request.method == 'POST':
        form = EquipoInstaladoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoInstaladoForm(instance=equipo)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Equipo: {equipo}', 'url_cancelar': reverse('lista_equipos'),
    })


# Vista para Eliminar un Equipo Instalado (DELETE mediante ORM, con confirmacion previa)
def eliminar_equipo(request, pk):
    equipo = get_object_or_404(EquipoInstalado, pk=pk)
    if request.method == 'POST':
        equipo.delete()
        return redirect('lista_equipos')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': equipo, 'titulo_entidad': 'Equipo', 'url_cancelar': reverse('lista_equipos'),
    })


# Vista para Consultar Panel de Tickets (RF-05)
# Filtros soportados: prioridad y estado del ticket
def lista_tickets(request):
    tickets = TicketSoporte.objects.select_related('equipo', 'equipo__cliente', 'tecnico').all().order_by('-fecha_creacion')

    prioridad = request.GET.get('prioridad')
    estado = request.GET.get('estado')

    if prioridad:
        tickets = tickets.filter(prioridad=prioridad)
    if estado:
        tickets = tickets.filter(estado=estado)

    return render(request, 'inventario/lista_tickets.html', {
        'tickets': tickets,
        'prioridades': TicketSoporte.PRIORIDADES,
        'estados': TicketSoporte.ESTADOS,
        'filtros': {
            'prioridad': prioridad,
            'estado': estado,
        },
    })


# Vista para Actualizar el Estado de un Ticket (UPDATE mediante ORM)
def editar_ticket(request, pk):
    ticket = get_object_or_404(TicketSoporte, pk=pk)
    if request.method == 'POST':
        form = TicketSoporteForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('lista_tickets')
    else:
        form = TicketSoporteForm(instance=ticket)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Ticket: {ticket}', 'url_cancelar': reverse('lista_tickets'),
    })


# Vista para Eliminar un Ticket de Soporte (DELETE mediante ORM, con confirmacion previa)
def eliminar_ticket(request, pk):
    ticket = get_object_or_404(TicketSoporte, pk=pk)
    if request.method == 'POST':
        ticket.delete()
        return redirect('lista_tickets')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': ticket, 'titulo_entidad': 'Ticket', 'url_cancelar': reverse('lista_tickets'),
    })


# Vista para Consultar una Categoría y listar sus Productos (Acceso Inverso via related_name)
def detalle_categoria(request, pk):
    """
    Usa prefetch_related('productos') para traer en una consulta optimizada
    la Categoría y todos los Productos asociados a ella (Acceso Inverso).
    """
    categoria = get_object_or_404(
        Categoria.objects.prefetch_related('productos'),
        pk=pk
    )
    
    return render(request, 'inventario/detalle_categoria.html', {
        'categoria': categoria
    })


# CRUD del modelo intermedio de la relación N:M (Producto <-> Proveedor vía Suministro)

# Vista para Crear un Suministro (agregar un Proveedor a un Producto, con sus atributos propios)
def crear_suministro(request, producto_pk):
    producto = get_object_or_404(Producto, pk=producto_pk)

    if request.method == 'POST':
        form = SuministroForm(request.POST)
        if form.is_valid():
            suministro = form.save(commit=False)
            suministro.producto = producto
            try:
                suministro.save()
                return redirect('productos_proveedores')
            except IntegrityError:
                form.add_error('proveedor', 'Este proveedor ya está registrado para este producto.')
    else:
        form = SuministroForm()

    return render(request, 'inventario/crear_suministro.html', {'form': form, 'producto': producto})


# Vista para Editar un Suministro (modificar los atributos propios de la relación N:M)
def editar_suministro(request, pk):
    suministro = get_object_or_404(Suministro, pk=pk)

    if request.method == 'POST':
        form = SuministroForm(request.POST, instance=suministro)
        if form.is_valid():
            try:
                form.save()
                return redirect('productos_proveedores')
            except IntegrityError:
                form.add_error('proveedor', 'Este proveedor ya está registrado para este producto.')
    else:
        form = SuministroForm(instance=suministro)

    return render(request, 'inventario/editar_suministro.html', {'form': form, 'objeto': suministro})


# Vista para Eliminar un Suministro (quitar un Proveedor de un Producto, con confirmación previa)
def eliminar_suministro(request, pk):
    suministro = get_object_or_404(Suministro, pk=pk)
    if request.method == 'POST':
        suministro.delete()
        return redirect('productos_proveedores')

    return render(request, 'inventario/eliminar_suministro.html', {'objeto': suministro})


class StockInsuficiente(Exception):
    pass


def sumar_meses(fecha, meses):
    mes = fecha.month - 1 + meses
    anio = fecha.year + mes // 12
    mes = mes % 12 + 1
    dia = min(fecha.day, calendar.monthrange(anio, mes)[1])
    return date(anio, mes, dia)


# Vista para Registrar una Instalación: crea un EquipoInstalado por cada número de serie (INSERT)
# y descuenta esa cantidad del stock del Producto (UPDATE). Todo o nada con transaction.atomic().
def registrar_instalacion(request):
    if request.method == 'POST':
        form = RegistrarInstalacionForm(request.POST)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cliente = form.cleaned_data['cliente']
            fecha = form.cleaned_data['fecha_instalacion']
            series = form.cleaned_data['numeros_serie']
            cantidad = len(series)

            try:
                with transaction.atomic():
                    # 1) INSERT de los equipos instalados
                    for serie in series:
                        EquipoInstalado.objects.create(
                            numero_serie=serie, producto=producto, cliente=cliente,
                            fecha_instalacion=fecha,
                            fin_garantia=sumar_meses(fecha, producto.meses_garantia),
                        )

                    # 2) UPDATE del stock con F().
                    filas = Producto.objects.filter(pk=producto.pk, stock__gte=cantidad).update(stock=F('stock') - cantidad)
                    if filas == 0:
                        
                        raise StockInsuficiente
            except StockInsuficiente:
                producto.refresh_from_db()
                form.add_error(None, f'Stock insuficiente de "{producto.nombre}": se solicitaron {cantidad} '
                                     f'unidad(es) y solo hay {producto.stock}. No se registró ningún cambio.')
            else:
                # Patrón Post/Redirect/Get: tras el exito se redirige para evitar reenvíos.
                messages.success(request, f'Instalación registrada: {cantidad} equipo(s) de "{producto.nombre}" '
                                          f'para {cliente}.')
                return redirect('registrar_instalacion')
    else:
        form = RegistrarInstalacionForm(initial={'fecha_instalacion': timezone.now().date()})

    return render(request, 'inventario/registrar_instalacion.html', {
        'form': form,
        'productos': Producto.objects.order_by('nombre'),
        'ultimos_equipos': EquipoInstalado.objects.select_related('producto', 'cliente').order_by('-id')[:5],
    })

def reporte(request):
    # Valor de cada suministro: precio_compra x stock del producto, calculado en la BD con F()
    valor = ExpressionWrapper(
        F('precio_compra') * F('producto__stock'),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )
    principales = Suministro.objects.filter(es_proveedor_principal=True)

    # Ejercicio 4: aggregate() devuelve un dict con el total global
    totales = principales.aggregate(
        valor_inventario=Sum(valor),
        suministros=Count('id'),
        unidades=Sum('producto__stock'),
    )
    detalle_valor = (principales.select_related('producto', 'proveedor')
                     .annotate(subtotal=valor).order_by('-subtotal'))

    # Ejercicio 5: annotate() agrega un valor calculado a cada objeto
    productos = Producto.objects.annotate(
        num_equipos=Count('equipos', distinct=True),
        num_proveedores=Count('proveedores', distinct=True),
    ).order_by('-num_equipos', '-num_proveedores', 'nombre')

    clientes = Cliente.objects.annotate(
        num_equipos=Count('equipos'),
        en_mantenimiento=Count('equipos', filter=Q(equipos__estado='MANTENIMIENTO')),
    ).order_by('-num_equipos', 'razon_social')

    # Ejercicio 5: values().annotate() agrupa por estado
    equipos_por_estado = list(EquipoInstalado.objects.values('estado').annotate(total=Count('id')).order_by('-total'))
    tickets_por_estado = list(TicketSoporte.objects.values('estado').annotate(total=Count('id')).order_by('-total', 'estado'))

    # Etiqueta legible y porcentaje de cada grupo (el porcentaje se formatea en el Template con floatformat)
    for grupos, estados in ((equipos_por_estado, EquipoInstalado.ESTADOS), (tickets_por_estado, TicketSoporte.ESTADOS)):
        etiquetas = dict(estados)
        total = sum(g['total'] for g in grupos)
        for g in grupos:
            g['etiqueta'] = etiquetas.get(g['estado'], g['estado'])
            g['porcentaje'] = g['total'] * 100 / total if total else 0

    return render(request, 'inventario/reporte.html', {
        'totales': totales,
        'detalle_valor': detalle_valor,
        'productos': productos,
        'clientes': clientes,
        'equipos_por_estado': equipos_por_estado,
        'tickets_por_estado': tickets_por_estado,
        'total_equipos': sum(g['total'] for g in equipos_por_estado),
        'total_tickets': sum(g['total'] for g in tickets_por_estado),
    })
