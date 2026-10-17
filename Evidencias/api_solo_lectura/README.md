# Ejercicio 7 – Recurso de solo lectura con relaciones anidadas

**Recurso:** `Cliente` con sus `EquipoInstalado` anidados (cada equipo muestra el nombre de su `Producto`).
(El proyecto no tiene `Pedido`; `Cliente → equipos` es su equivalente 1:N.)

- Serializer: `ClienteConEquiposSerializer` + `EquipoAnidadoSerializer` (`inventario/serializer.py`)
- Vista: `ClienteConEquiposViewSet(ReadOnlyModelViewSet)` (`inventario/views/clientes.py`)
- Ruta: `GET /api/clientes-equipos/` y `GET /api/clientes-equipos/<id>/` (POST/PUT/DELETE → 405)

```python
def get_queryset(self):
    return Cliente.objects.order_by('id').prefetch_related(
        Prefetch('equipos', queryset=EquipoInstalado.objects.select_related('producto'))
    )
```

`prefetch_related` para `equipos` (relación inversa 1:N) y `select_related('producto')` dentro del
Prefetch (FK, se resuelve con JOIN).

## Medición (`python manage.py medir_consultas_clientes`, con `connection.queries`)

| Queryset | Consultas (3 clientes) |
|---|---|
| ANTES: `Cliente.objects.all()` | **18** (1 clientes + 3 equipos por cliente + 14 productos, uno por equipo) |
| DESPUÉS: `prefetch_related` + `select_related` | **2** (1 clientes + 1 equipos con JOIN a producto) |

Antes crece como 1 + N + M (clientes y equipos); después es constante: 2 consultas sin importar cuántos registros haya.
