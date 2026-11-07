# Laboratorio 10 – Ejercicio 3: Pasar datos con props y armar la lista

## Qué se hizo
- `ProductoCard` ahora **recibe sus datos por props** (desestructuradas en el parámetro): `nombre, marca, modelo, categoria, precio, stock`.
- `marca` tiene **valor por defecto** (`'Sin marca'`): si el padre no envía la prop, se muestra ese texto.
- Nuevo componente `ListaProductos`: recibe el arreglo `productos`, muestra el mensaje "No hay registros" si está vacío y recorre con `map()` creando un `<ProductoCard key={p.id} ... />` por registro.
- `App.jsx` solo compone: `<ListaProductos productos={productos} />` y una tarjeta de prueba sin `marca`.

## Correspondencia API → props
| Campo de la API | Prop del componente |
|---|---|
| `nombre` | `nombre` |
| `marca` | `marca` (default `'Sin marca'`) |
| `modelo` | `modelo` |
| `categoria.nombre` | `categoria` |
| `precio_base` | `precio` |
| `stock` | `stock` |

## Verificación
- `npm run lint`: sin errores (exit 0).
- `npm run build`: compila correctamente.
- Consola del navegador: sin warnings ni errores (la `key` está bien puesta).
- Resultado: 5 productos en la lista; "¡Últimas unidades!" (stock 3 y 2), "Agotado" (stock 0); la tarjeta de prueba muestra "Sin marca".

## Capturas
- `captura_codigo_ProductoCard.jsx.png`, `captura_codigo_ListaProductos.jsx.png`, `captura_codigo_App.jsx.png`
- `captura_pagina_resultado.png`
