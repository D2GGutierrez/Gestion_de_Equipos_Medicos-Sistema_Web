from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import TicketSoporteForm
from ..models import TicketSoporte


# Vista para Consultar Panel de Tickets (RF-05)
# Filtros soportados: prioridad y estado del ticket
# Vistas rápidas del panel: cada una es una regla de negocio de TicketSoporteQuerySet (se pueden encadenar)
VISTAS_TICKETS = {
    'pendientes': ('Pendientes', lambda qs: qs.pendientes()),
    'urgentes': ('Urgentes sin resolver', lambda qs: qs.pendientes().urgentes()),
    'sin_tecnico': ('Pendientes sin técnico', lambda qs: qs.pendientes().sin_tecnico()),
    'mes': ('Reportados este mes', lambda qs: qs.creados_en_mes()),
    'atendidos': ('Atendidos', lambda qs: qs.atendidos()),
}


def lista_tickets(request):
    tickets = TicketSoporte.objects.con_detalle()

    vista = request.GET.get('vista')
    if vista in VISTAS_TICKETS:
        tickets = VISTAS_TICKETS[vista][1](tickets)

    prioridad = request.GET.get('prioridad')
    estado = request.GET.get('estado')

    if prioridad:
        tickets = tickets.filter(prioridad=prioridad)
    if estado:
        tickets = tickets.filter(estado=estado)

    return render(request, 'inventario/lista_tickets.html', {
        'tickets': tickets.recientes(),
        'prioridades': TicketSoporte.PRIORIDADES,
        'estados': TicketSoporte.ESTADOS,
        'vistas': [(clave, etiqueta) for clave, (etiqueta, _) in VISTAS_TICKETS.items()],
        'filtros': {
            'vista': vista,
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



# ---------------------------------------------------------------------------
# Ejercicio 12 - API de solo lectura: Tickets con equipo (cliente, producto) y tecnico anidados
# ---------------------------------------------------------------------------
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import TicketSoporte
from ..serializer import TicketDetalleSerializer


class TicketDetalleViewSet(viewsets.ReadOnlyModelViewSet):
    """Solo GET. Búsqueda, ordenamiento, filtros por parámetro y una acción propia (Ejercicio 13)."""
    serializer_class = TicketDetalleSerializer

    # ?search=... busca en estos campos; ?ordering=prioridad (o -fecha_creacion) ordena
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['codigo_ticket', 'descripcion_falla', 'equipo__numero_serie']
    ordering_fields = ['id', 'fecha_creacion', 'prioridad', 'estado']

    def get_queryset(self):
        # Todas son FK (N:1) -> select_related resuelve todo con JOINs en UNA consulta.
        qs = TicketSoporte.objects.select_related(
            'equipo__cliente', 'equipo__producto', 'tecnico'
        ).order_by('-fecha_creacion')

        # Filtros por parámetro: ?estado=ABIERTO  y  ?prioridad=ALTA
        estado = self.request.query_params.get('estado')
        if estado:
            qs = qs.filter(estado=estado.upper())
        prioridad = self.request.query_params.get('prioridad')
        if prioridad:
            qs = qs.filter(prioridad=prioridad.upper())
        return qs

    # GET /api/tickets-detalle/urgentes-pendientes/
    @action(detail=False, methods=['get'], url_path='urgentes-pendientes')
    def urgentes_pendientes(self, request):
        """Tickets abiertos/en proceso de prioridad alta o crítica.
        Reutiliza TicketSoporteQuerySet (Semana 7): pendientes().urgentes()."""
        qs = self.filter_queryset(self.get_queryset()).pendientes().urgentes()
        return Response(self.get_serializer(qs, many=True).data)
