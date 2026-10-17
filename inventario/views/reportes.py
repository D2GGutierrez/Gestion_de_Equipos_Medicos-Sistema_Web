from datetime import timedelta

from django.db.models import Avg, Count, DecimalField, ExpressionWrapper, F, Max, Min, Q, Sum
from django.shortcuts import render
from django.utils import timezone

from ..models import (
    Cliente, EquipoInstalado, Producto, ProductoQuerySet, Suministro, TicketSoporte, TicketSoporteQuerySet, Usuario,
)


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
    productos = Producto.objects.con_conteos().order_by('-num_equipos', '-num_proveedores', 'nombre')

    # Reglas de negocio encadenadas: productos que requieren reposición
    stock_bajo = Producto.objects.stock_bajo().por_nombre()
    agotados = Producto.objects.agotados().por_nombre()
    instalados_mes = Producto.objects.instalados_en_mes().con_conteos().por_nombre()

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
        'stock_bajo': stock_bajo,
        'agotados': agotados,
        'instalados_mes': instalados_mes,
        'stock_minimo': ProductoQuerySet.STOCK_MINIMO,
    })


# Reportes de la investigación: soporte postventa (garantías, tickets, técnicos y proveedores)
# Reglas de ticket pendiente/urgente/atendido como Q, definidas una sola vez en TicketSoporteQuerySet
T = TicketSoporteQuerySet
DIAS_AVISO_GARANTIA = 90


def reporte_postventa(request):
    hoy = timezone.localdate()
    limite_aviso = hoy + timedelta(days=DIAS_AVISO_GARANTIA)

    # Reporte 1 · aggregate(): resumen global de garantías y tickets (cada uno devuelve un dict)
    garantias = EquipoInstalado.objects.aggregate(
        total=Count('id'),
        vigentes=Count('id', filter=Q(fin_garantia__gte=hoy)),
        vencidas=Count('id', filter=Q(fin_garantia__lt=hoy)),
        por_vencer=Count('id', filter=Q(fin_garantia__gte=hoy, fin_garantia__lte=limite_aviso)),
        proximo_vencimiento=Min('fin_garantia', filter=Q(fin_garantia__gte=hoy)),
    )
    garantias['pct_vigentes'] = garantias['vigentes'] * 100 / garantias['total'] if garantias['total'] else 0

    tickets = TicketSoporte.objects.aggregate(
        total=Count('id'),
        pendientes=Count('id', filter=T.q_pendiente()),
        criticos_pendientes=Count('id', filter=T.q_pendiente() & T.q_urgente()),
        sin_tecnico=Count('id', filter=T.q_pendiente() & Q(tecnico__isnull=True)),
    )
    tickets['pct_pendientes'] = tickets['pendientes'] * 100 / tickets['total'] if tickets['total'] else 0

    equipos_por_vencer = (EquipoInstalado.objects.select_related('producto', 'cliente')
                          .filter(fin_garantia__gte=hoy, fin_garantia__lte=limite_aviso).order_by('fin_garantia'))

    # Reporte 2 · annotate(): carga de trabajo de cada técnico
    tecnicos = Usuario.objects.filter(rol='TECNICO').annotate(
        asignados=Count('tickets_asignados'),
        pendientes=Count('tickets_asignados', filter=T.q_pendiente('tickets_asignados__')),
        urgentes=Count('tickets_asignados', filter=T.q_pendiente('tickets_asignados__') & T.q_urgente('tickets_asignados__')),
        atendidos=Count('tickets_asignados', filter=T.q_atendido('tickets_asignados__')),
    ).order_by('-pendientes', '-urgentes', 'nombre_completo')

    # Reporte 3 · annotate(): situación postventa de cada cliente (dos relaciones -> distinct=True)
    clientes = Cliente.objects.annotate(
        equipos_total=Count('equipos', distinct=True),
        garantia_vencida=Count('equipos', filter=Q(equipos__fin_garantia__lt=hoy), distinct=True),
        tickets_pendientes=Count('equipos__tickets', filter=T.q_pendiente('equipos__tickets__'), distinct=True),
    ).order_by('-tickets_pendientes', '-garantia_vencida', 'razon_social')

    # Reporte 4 · values().annotate(): tickets agrupados por prioridad
    etiquetas_prioridad = dict(TicketSoporte.PRIORIDADES)
    por_prioridad = list(
        TicketSoporte.objects.values('prioridad')
        .annotate(total=Count('id'), pendientes=Count('id', filter=T.q_pendiente()))
        .order_by('-pendientes', '-total')
    )
    for fila in por_prioridad:
        fila['etiqueta'] = etiquetas_prioridad.get(fila['prioridad'], fila['prioridad'])

    # Métodos encadenados del QuerySet: tickets urgentes que siguen sin resolver, del más reciente al más antiguo
    urgentes_pendientes = TicketSoporte.objects.pendientes().urgentes().con_detalle().recientes()

    # Reporte 5 · values().annotate(): desempeño de proveedores a partir del modelo intermedio Suministro
    proveedores = (
        Suministro.objects.values('proveedor__nombre_empresa')
        .annotate(
            productos=Count('producto'),
            como_principal=Count('id', filter=Q(es_proveedor_principal=True)),
            dias_entrega=Avg('dias_entrega_promedio'),
            entrega_mas_lenta=Max('dias_entrega_promedio'),
        )
        .order_by('dias_entrega', '-productos')
    )

    return render(request, 'inventario/reporte_postventa.html', {
        'hoy': hoy,
        'dias_aviso': DIAS_AVISO_GARANTIA,
        'garantias': garantias,
        'tickets': tickets,
        'equipos_por_vencer': equipos_por_vencer,
        'tecnicos': tecnicos,
        'clientes': clientes,
        'por_prioridad': por_prioridad,
        'proveedores': proveedores,
        'urgentes_pendientes': urgentes_pendientes,
    })
