# Ejercicio 12 – Recurso de solo lectura con relaciones anidadas (Tickets)

**Recurso:** `TicketSoporte` con el equipo (y su cliente y producto) y el técnico anidados.
- Serializers: `TicketDetalleSerializer` → `EquipoMiniSerializer` (cliente, producto) y `TecnicoMiniSerializer` (`inventario/serializer.py`)
- Vista: `TicketDetalleViewSet(ReadOnlyModelViewSet)` (`inventario/views/tickets.py`)
- Ruta: `GET /api/tickets-detalle/` y `/api/tickets-detalle/<id>/` (POST → 405)

```python
def get_queryset(self):
    return TicketSoporte.objects.select_related(
        'equipo__cliente', 'equipo__producto', 'tecnico'
    ).order_by('-fecha_creacion')
```
Todas las relaciones son FK (N:1), por eso corresponde `select_related` (JOINs en una sola consulta).

## Medición (`python manage.py medir_consultas_tickets`, usando `connection.queries`, 8 tickets)

| Queryset | Consultas |
|---|---|
| ANTES: `TicketSoporte.objects.all()` | **33** (1 tickets + equipo + cliente + producto + técnico por cada ticket) |
| DESPUÉS: `select_related('equipo__cliente', 'equipo__producto', 'tecnico')` | **1** |

Sin optimizar, el número crece con cada ticket (≈ 1 + 4·N); optimizado se queda en 1 sin importar cuántos haya.
