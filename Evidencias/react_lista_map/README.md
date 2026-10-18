# Ejercicio 5 – Lista con `map()` y `key`

`src/App.jsx` define un arreglo `productos` con 5 registros, con la misma forma que `GET /api/productos/` (Semana 8):
los decimales son texto (`precio_base: '4500.5'`, `'6.5'`) y la categoría va anidada. Se muestran así:

```jsx
<ul>
  {productos.map((p) => (
    <li key={p.id}>
      <strong>{p.nombre}</strong> — {p.marca} {p.modelo} · {p.categoria.nombre} ·
      S/ {Number(p.precio_base).toFixed(2)} · Stock: {p.stock}
    </li>
  ))}
</ul>
```

- `Number(p.precio_base).toFixed(2)`: el texto `"4500.5"` se convierte a número y se muestra con 2 decimales (`4500.50`). Sin `Number(...)`, `.toFixed` falla porque un texto no tiene ese método.
- `key={p.id}`: identificador estable y único que React usa para saber qué elemento es cuál cuando la lista cambia. No se usa el índice del arreglo porque cambia si se reordena o se elimina un registro. En la consola del navegador no apareció ninguna advertencia de `key`.

## Resultado (`captura_pagina.png`)
Cinco filas: Ecógrafo Doppler Color S/ 18500.00 · Monitor de Signos Vitales S/ 4500.50 · Ventilador Mecánico S/ 32000.00 · Desfibrilador Bifásico S/ 9800.75 · Oxímetro de Pulso S/ 6.50.

## ¿Qué equivale a `map()` en los Templates de Django?
Al `{% for %}`:

```django
<ul>
  {% for p in productos %}
    <li>{{ p.nombre }} — S/ {{ p.precio_base }}</li>
  {% endfor %}
</ul>
```

Los dos recorren una colección y repiten un bloque de HTML por cada elemento (`p` es el elemento actual en ambos). Diferencias:
- En Django es una etiqueta del template; en React `map()` es un método normal de JavaScript que devuelve una lista de elementos JSX, y va dentro de `{ }`.
- React exige la `key` en cada elemento; `{% for %}` no la necesita porque el servidor genera el HTML completo cada vez, mientras que React compara lo que ya está en pantalla con lo nuevo.
- Lo que en Django sería el filtro `{{ p.precio_base|floatformat:2 }}` aquí es `Number(...).toFixed(2)`.

Nota: los datos son representativos de la forma de la API (no se leyeron de la API).
