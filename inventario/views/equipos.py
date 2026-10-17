import calendar
from datetime import date

from django.contrib import messages
from django.db import transaction
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone

from ..forms import EquipoInstaladoForm, RegistrarInstalacionForm
from ..models import Cliente, EquipoInstalado, Producto


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
                    filas = Producto.objects.filter(pk=producto.pk).con_stock_para(cantidad).update(stock=F('stock') - cantidad)
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
        'productos': Producto.objects.por_nombre(),
        'ultimos_equipos': EquipoInstalado.objects.select_related('producto', 'cliente').order_by('-id')[:5],
    })
