# Ejercicio 12 – Relación anidada en la investigación propia

**Relación mostrada: 1:N Cliente → equipos instalados** (`frontend/src/App.jsx`, arreglo `clientes`, con la forma de `GET /api/clientes-equipos/`: cada cliente trae su arreglo `equipos` dentro).

```jsx
// Total por cliente, calculado con JavaScript (texto -> número con Number)
function totalCliente(cliente) {
  return cliente.equipos.reduce((suma, e) => suma + Number(e.precio_base), 0)
}

{clientes.map((c) => (                                   // map() externo, key = id del cliente
  <li key={c.id} className="tarjeta">
    <strong>{c.razon_social}</strong> ({c.equipos.length} {c.equipos.length === 1 ? 'equipo' : 'equipos'})   {/* conteo */}
    <ul className="equipos">
      {c.equipos.map((e) => (                            // map() interno, key = id del equipo
        <li key={e.id}>{e.numero_serie} — {e.producto_nombre} · {e.estado} · S/ {Number(e.precio_base).toFixed(2)}</li>
      ))}
    </ul>
    <p style={{ fontWeight: 'bold', color: '#065f46' }}>Total de equipos: S/ {totalCliente(c).toFixed(2)}</p>
  </li>
))}
```

| Cliente | Conteo (`length`) | Total (`reduce`) |
|---|---|---|
| Clínica San Gabriel S.A. | 3 equipos | S/ 32801.25 |
| Hospital Regional de Arequipa | 2 equipos | S/ 64000.00 |
| Centro Médico Santa Rosa E.I.R.L. | 1 equipo | S/ 6.50 |

`captura_pagina.png` muestra la sección "Clientes y sus equipos instalados" (junto a la lista de productos). Cada nivel tiene su `key` basada en el `id`, y no hay advertencias en la consola.
(El modelo intermedio `Suministro`, Producto ↔ Proveedor, no se muestra: se eligió la relación 1:N.)
