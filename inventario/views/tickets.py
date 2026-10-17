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
