# Ejercicio 13 – Filtros y acción propia (Tickets)

Se amplió `TicketDetalleViewSet` (`inventario/views/tickets.py`):
- `SearchFilter`: `search_fields = ['codigo_ticket', 'descripcion_falla', 'equipo__numero_serie']`
- `OrderingFilter`: `ordering_fields = ['id', 'fecha_creacion', 'prioridad', 'estado']`
- Filtros por parámetro en `get_queryset()`: `?estado=` y `?prioridad=`
- `@action(detail=False)` `urgentes-pendientes`: reutiliza `TicketSoporteQuerySet` de la Semana 7 → `pendientes().urgentes()`

## URLs probadas (8 tickets en la BD)

| # | URL | Resultado |
|---|---|---|
| 1 | `/api/tickets-detalle/?search=ECO` | 200 · 1 ticket: TCK-0008 (equipo ECO-0001) |
| 2 | `/api/tickets-detalle/?estado=abierto&ordering=prioridad` | 200 · 4 tickets ABIERTO, ordenados por prioridad (alfabético): TCK-0005 ALTA, TCK-0002 CRITICA, TCK-0003 MEDIA, TCK-0008 MEDIA |
| 3 | `/api/tickets-detalle/urgentes-pendientes/` | 200 · 3 tickets: TCK-0005 (ALTA, ABIERTO), TCK-0002 (CRITICA, ABIERTO), TCK-0001 (ALTA, EN_PROCESO) |
| 4 | `/api/tickets-detalle/urgentes-pendientes/?ordering=-fecha_creacion&search=MON` | 200 · 1 ticket: TCK-0001 (equipo MON-0103) |

Nota: la URL 2 combina parámetros con `&`; la 4 combina la acción propia con búsqueda y orden.
`ordering=prioridad` ordena el texto alfabéticamente (ALTA < CRITICA < MEDIA), no por gravedad.
