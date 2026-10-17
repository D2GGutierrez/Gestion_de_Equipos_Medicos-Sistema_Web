from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import ClienteForm
from ..models import Cliente


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


# ---------------------------------------------------------------------------
# Ejercicios 7 y 8 - API de solo lectura: Clientes con sus equipos instalados anidados
# ---------------------------------------------------------------------------
from django.db.models import Prefetch
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import Cliente, EquipoInstalado, TicketSoporte
from ..serializer import ClienteConEquiposSerializer


class ClienteConEquiposViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo list y retrieve (GET). POST/PUT/DELETE devuelven 405."""
    serializer_class = ClienteConEquiposSerializer

    def get_queryset(self):
        equipos = EquipoInstalado.objects.select_related('producto')
        qs = Cliente.objects.order_by('id')

        estado = self.request.query_params.get('estado')
        if estado:
            estado = estado.upper()
            equipos = equipos.filter(estado=estado)          
            qs = qs.filter(equipos__estado=estado).distinct()

        # prefetch_related (1:N inverso) + select_related('producto') dentro del Prefetch
        return qs.prefetch_related(Prefetch('equipos', queryset=equipos))

    # GET /api/clientes-equipos/con-tickets-urgentes/
    @action(detail=False, methods=['get'], url_path='con-tickets-urgentes')
    def con_tickets_urgentes(self, request):
        """Clientes con tickets pendientes y urgentes. Reutiliza TicketSoporteQuerySet (Semana 7)."""
        tickets = TicketSoporte.objects.pendientes().urgentes()
        clientes = self.get_queryset().filter(equipos__tickets__in=tickets).distinct()
        return Response(self.get_serializer(clientes, many=True).data)


# ---------------------------------------------------------------------------
# Ejercicio 11 - CRUD completo del recurso Cliente con ModelViewSet (/api/clientes/)
# ---------------------------------------------------------------------------
from ..serializer import ClienteSerializer


class ClienteViewSet(viewsets.ModelViewSet):
    """list/create/retrieve/update/partial_update/destroy -> 200, 201, 400, 404, 204."""
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer
