# Ejercicio 7 – Relación 1:N con listas anidadas

**Relación:** un Cliente tiene muchos equipos instalados (`Cliente 1 → N EquipoInstalado`), con la forma de `GET /api/clientes-equipos/` (Semana 8): cada cliente trae un arreglo `equipos` dentro, y los decimales llegan como texto.

```jsx
const clientes = [
  { id: 1, razon_social: 'Clínica San Gabriel S.A.',
    equipos: [ { id: 11, numero_serie: 'ECO-0001', ..., precio_base: '18500.00' }, ... ] },
  ...
]

function totalCliente(cliente) {
  return cliente.equipos.reduce((suma, e) => suma + Number(e.precio_base), 0)
}

{clientes.map((c) => (                      // map() externo: key = id del cliente
  <li key={c.id}>
    <strong>{c.razon_social}</strong> ({c.equipos.length} {c.equipos.length === 1 ? 'equipo' : 'equipos'})
    <ul>
      {c.equipos.map((e) => (               // map() interno: key = id del equipo
        <li key={e.id}>{e.numero_serie} — {e.producto_nombre} · {e.estado} · S/ {Number(e.precio_base).toFixed(2)}</li>
      ))}
    </ul>
    <p>Total de equipos: S/ {totalCliente(c).toFixed(2)}</p>
  </li>
))}
```

- Cada `map()` tiene su propia `key` con el `id` de su nivel; los ids de clientes (1, 2, 3) y de equipos (11, 12, …) no se repiten entre hermanos.
- El total se calcula con JavaScript (`reduce` suma el precio de los equipos de cada cliente; `Number(...)` convierte los textos).

## Resultado (`captura_pagina.png`)
| Cliente | Equipos | Total mostrado | Comprobación |
|---|---|---|---|
| Clínica San Gabriel S.A. | 3 | S/ 32801.25 | 18500.00 + 4500.50 + 9800.75 |
| Hospital Regional de Arequipa | 2 | S/ 64000.00 | 32000.00 + 32000.00 |
| Centro Médico Santa Rosa E.I.R.L. | 1 | S/ 6.50 | 6.50 |

Sin advertencias de React en la consola. En Django equivale a un `{% for %}` dentro de otro `{% for %}` (o `cliente.equipos.all`).
Nota: los datos son representativos de la forma de la API (no se leyeron de ella).
