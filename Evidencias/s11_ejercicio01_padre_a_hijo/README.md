# Laboratorio 11 – Ejercicio 1: Pasar datos del padre al hijo

## Qué se hizo
Dentro de `frontend/src/practica/` se creó la práctica de la cafetería:

| Archivo | Rol |
|---|---|
| `datos.js` | Cinco productos con `id`, `nombre`, `precio` (**texto**, como la API) y `stock` |
| `Practica.jsx` | **Padre**: importa los datos y los entrega a `Catalogo` con `productos={productos}` |
| `Catalogo.jsx` | Recibe el arreglo por props y entrega **cada producto** a `ProductoCard` con `map()` y `key={p.id}` |
| `ProductoCard.jsx` | Recibe un `producto` por props; muestra el nombre, el precio con `Number(...).toFixed(2)` y «Agotado» cuando `stock === 0` (con `&&`) |

Flujo de los datos: `Practica` → (`productos`) → `Catalogo` → (`producto`) → `ProductoCard`. Los datos bajan por props.

`App.jsx` muestra la práctica en una sección propia (`<Practica />` dentro de `Tarjeta`), debajo de lo hecho en el Laboratorio 10.

## Resultado en el navegador
| Producto | Precio mostrado | Stock |
|---|---|---|
| Café americano | S/ 6.50 | 50 |
| Capuchino | S/ 9.00 | 40 |
| Torta de chocolate | S/ 10.50 | 5 |
| Jugo de naranja | S/ 7.00 **Agotado** | 0 |
| Tostada | S/ 4.50 | 10 |

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola del navegador sin errores ni warnings.

## Capturas
- Código: `captura_codigo_Practica.jsx.png`, `captura_codigo_Catalogo.jsx.png`, `captura_codigo_ProductoCard.jsx.png`, `captura_codigo_datos.js.png`
- Página: `captura_pagina_resultado.png`; estructura de carpetas: `captura_estructura_carpetas.png`
