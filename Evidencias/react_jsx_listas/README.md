# Ejercicio 10 – JSX y listas de la investigación propia

`frontend/src/App.jsx` contiene los arreglos de **dos entidades** de la aplicación, con la forma de la respuesta de la API (decimales como texto, objetos anidados):

| Entidad | Arreglo | Forma de la API | `map()` y `key` |
|---|---|---|---|
| Producto | `productos` (5 registros) | `GET /api/productos/`: `id`, `codigo_sku`, `nombre`, `marca`, `modelo`, `precio_base: '4500.5'`, `meses_garantia`, `stock`, `categoria: { id, nombre }` | `productos.map((p) => <li key={p.id}>…)` |
| Cliente (con sus equipos instalados) | `clientes` (3 registros) | `GET /api/clientes-equipos/`: `id`, `razon_social`, `equipos: [ { id, numero_serie, estado, producto_nombre, precio_base } ]` | `clientes.map((c) => <li key={c.id}>…)` y, dentro, `c.equipos.map((e) => <li key={e.id}>…)` |

## Expresiones entre llaves usadas
- Variables y propiedades: `{p.nombre}`, `{p.marca} {p.modelo}`, `{p.categoria.nombre}`, `{c.razon_social}`
- Conversión y formato: `{Number(p.precio_base).toFixed(2)}`
- Cálculos y funciones: `{productos.length}`, `{c.equipos.length}`, `{totalCliente(c).toFixed(2)}`
- Condicionales: ternario `{p.stock > 0 ? ... : 'Agotado'}` y `&&` para `¡Últimas unidades!` y `No hay registros`

## Comprobación
La página (`captura_pagina.png`) muestra las 5 tarjetas de productos y las 3 de clientes con sus equipos anidados, y la consola del navegador no muestra advertencias (ni de `key`). Todos los `<li>` generados con `map()` llevan `key` basada en el `id` de su registro.
