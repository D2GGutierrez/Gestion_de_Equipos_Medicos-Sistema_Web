# Ejercicio 4 – Primer JSX con expresiones

Se vaciaron `src/App.css` y `src/index.css` y se reemplazó `src/App.jsx` (código en `App.jsx` / `captura_codigo_App.jsx.png`).

## Expresiones con llaves `{ }`
| Expresión | Tipo | Resultado en pantalla |
|---|---|---|
| `{nombreApp}` | variable | Gestión de Equipos Médicos (en el `<h1>`) |
| `{equipo}` | variable | Monitor de Signos Vitales |
| `{precioBase.toFixed(2)}` | método de número | S/ 4500.00 |
| `{precioConImpuesto(precioBase).toFixed(2)}` | llamada a función + cálculo (IGV 18 %) | S/ 5310.00 |
| `{2 * 12}` | cálculo | 24 meses |

Dentro de `{ }` va cualquier expresión de JavaScript (variable, operación o llamada a función), no sentencias como `if` o `for`.

## Página en el navegador
`captura_pagina.png` (http://localhost:5173/): sin estilos, porque los CSS están vacíos.
