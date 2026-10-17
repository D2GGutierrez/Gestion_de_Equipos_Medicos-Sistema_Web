# Ejercicio 8 – Búsqueda, ordenamiento, filtro por parámetro y acción propia

## Cambios
- `CategoriaViewSet` (recurso simple): `SearchFilter` + `OrderingFilter`, `search_fields = ['nombre', 'descripcion']`, `ordering_fields = ['id', 'nombre']`.
- `ClienteConEquiposViewSet` (recurso con relaciones): `get_queryset()` filtra por `?estado=` (estado del `EquipoInstalado`: OPERATIVO, MANTENIMIENTO, INACTIVO) y filtra también los equipos anidados.
- Acción `@action(detail=False)` `con-tickets-urgentes`: reutiliza `TicketSoporte.objects.pendientes().urgentes()` (QuerySet personalizado de la Semana 7).

## URLs probadas (datos actuales de la BD)

| # | URL | Resultado |
|---|---|---|
| 1 | `/api/categorias/?search=mon` | 1 categoría: *Monitoreo de Pacientes* (de 5) |
| 2 | `/api/categorias/?ordering=-nombre` | 5 categorías de Z a A: Soporte Vital, Monitoreo de Pacientes, Insumos Médicos, Equipos de Diagnóstico, Diagnóstico por Imagen |
| 3 | `/api/clientes-equipos/?estado=mantenimiento` | 2 clientes, solo con sus equipos en mantenimiento: Clínica San Gabriel (DES-0302) y Hospital Regional de Arequipa (MON-0103, VEN-0202) |
| 4 | `/api/clientes-equipos/con-tickets-urgentes/` | 1 cliente: Hospital Regional de Arequipa (6 equipos) |
| 5 | `/api/clientes-equipos/con-tickets-urgentes/?estado=OPERATIVO` | 1 cliente: Hospital Regional de Arequipa, solo equipos OPERATIVO (VEN-0201, RX-0501, MON-0201, MON-0202) |
| 6 | `/api/categorias/?search=equipos&ordering=-nombre` | 4 categorías (combina `&`): las que contienen "equipos", ordenadas Z→A (Soporte Vital, Monitoreo de Pacientes, Equipos de Diagnóstico, Diagnóstico por Imagen) |

(Sin parámetros, `/api/clientes-equipos/` devuelve los 3 clientes con todos sus equipos.)
