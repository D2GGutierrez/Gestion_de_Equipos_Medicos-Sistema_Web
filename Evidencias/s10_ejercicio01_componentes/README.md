# Laboratorio 10 – Ejercicio 1: Recuperar el proyecto e identificar los componentes

## Punto de partida
Se retomó el proyecto de React de la Semana 9 (`frontend/`) y se ejecutó `npm run dev` (VITE v8.3.4, http://localhost:5173/). La página funciona igual que antes: 5 productos y 3 clientes con sus equipos, sin advertencias en la consola (`captura_pagina_npm_run_dev.png`).

## Los tres fragmentos de `App.jsx` que se convertirán en componentes
Marcados en `captura_candidatos_App.jsx.png` (líneas de `App.jsx` tras mover los datos).

| # | Fragmento (líneas) | Componente propuesto | Por qué conviene convertirlo |
|---|---|---|---|
| 1 | La tarjeta de un producto: el `<li key={p.id} className="tarjeta">` con nombre, marca, modelo, categoría, precio y stock (21–28) | `ProductoCard` | Es la unidad más pequeña que se repite: el mismo bloque se dibuja una vez por producto, y solo cambian los datos (nombre, precio, stock). Recibirá esos datos por props, y es donde después irá el botón con estado y su contador propio (ejercicio 6). |
| 2 | La lista de productos: el título con el conteo, el mensaje "No hay registros" y el `<ul>` con el `map()` (14–30) | `ListaProductos` | Tiene una responsabilidad distinta a la tarjeta: recibe el arreglo completo, decide qué mostrar si está vacío y crea un `ProductoCard` por cada elemento con su `key`. Es también el lugar natural para el campo de búsqueda que filtra la lista (ejercicio 7). |
| 3 | El detalle de la relación 1:N: el `<li>` de cada cliente con su lista de equipos y el total (39–51) | `ClienteCard` (y dentro, `EquipoItem` para cada equipo) | Combina datos de dos niveles (cliente y equipos anidados) y un cálculo (el total). Separarlo evita tener `map()` dentro de `map()` en `App.jsx`, y el equipo anidado es a su vez un fragmento repetido (`EquipoItem`) que se puede reutilizar. |

Resultado esperado: `App.jsx` queda como un resumen de la pantalla, con `<ListaProductos productos={productos} />` y la lista de `<ClienteCard />`, en lugar de un solo bloque grande.

## Cambios hechos en este ejercicio
- Se creó la carpeta `src/components/` (con un `.gitkeep`, porque Git no guarda carpetas vacías; se borrará cuando haya componentes).
- Se movieron los datos escritos a mano a `src/datos.js` (`export const productos` y `export const clientes`) y `App.jsx` los importa: `import { productos, clientes } from './datos.js'`. La función `totalCliente` se queda por ahora en `App.jsx`; irá con `ClienteCard` en el ejercicio 5.
- No se creó ningún componente todavía (eso empieza en el ejercicio 2).

## Estructura de carpetas (`captura_estructura_carpetas.png`)
```
frontend/
├── index.html
├── package.json
├── vite.config.js
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── App.css
    ├── index.css
    ├── datos.js          <- nuevo
    ├── components/       <- nueva (vacía por ahora)
    └── assets/
```
Comprobación tras el cambio: `npm run lint` sin avisos y `npm run build` correcto.

En Django, esta división equivale a pasar de una plantilla grande a varios `{% include %}`: cada componente es un trozo reutilizable de la interfaz que recibe sus datos desde fuera.
