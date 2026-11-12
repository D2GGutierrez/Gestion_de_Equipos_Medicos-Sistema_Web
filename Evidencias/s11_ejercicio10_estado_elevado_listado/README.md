# Laboratorio 11 – Ejercicio 10: Estado elevado y listado del panel

Entidad principal del panel: **Equipo instalado** (definida en el Ejercicio 9).

## Qué se hizo
| Archivo | Rol |
|---|---|
| `src/datosPanel.js` | Los **14 equipos** reales de la base de datos, escritos a mano con la forma de `GET /api/equipos/` (`id`, `numero_serie`, `fecha_instalacion`, `fin_garantia`, `estado`, `producto`, `producto_nombre`, `cliente`, `cliente_razon_social`) |
| `src/components/PanelEquipos.jsx` | **Padre**: `const [equipos] = useState(equiposIniciales)`; es el único lugar donde vive el arreglo y se lo entrega al listado por props |
| `src/components/ListadoEquipos.jsx` | Recibe `equipos` por props y dibuja una fila por cada uno con `map()` y `key={e.id}`; muestra «No hay equipos registrados» con `&&` si el arreglo está vacío |
| `src/components/FilaEquipo.jsx` | Recibe **un** `equipo` por props: serie, producto, estado (etiqueta de color), cliente y fechas |

Cada componente está en su archivo de `src/components`, con nombre en mayúscula. `App.jsx` muestra el panel en la sección «Panel administrativo: equipos instalados».

Flujo: `PanelEquipos` → (`equipos`) → `ListadoEquipos` → (`equipo`) → `FilaEquipo`. Los datos bajan por props; el estado se elevó al padre para poder compartirlo luego con el resumen, el buscador y el formulario. (`setEquipos` se agrega en los ejercicios 11 y 12, cuando haya acciones que lo cambien.)

## Resultado en el navegador
Se muestran **14 equipos** (`Equipos instalados (14)`): 9 operativos, 3 en mantenimiento y 2 inactivos (el conteo por estado en pantalla se calcula en el Ejercicio 13). Cada fila muestra serie, producto, estado, cliente, fecha de instalación y fin de garantía.

## Verificación
- `npm run lint`: sin advertencias ni errores (código 0). `npm run build`: compila (código 0).
- Consola del navegador sin errores ni warnings (cada fila lleva `key` con el `id`).

## Capturas
`captura_codigo_PanelEquipos.jsx.png`, `captura_codigo_ListadoEquipos.jsx.png`, `captura_codigo_FilaEquipo.jsx.png`, `captura_codigo_datosPanel.js.png`, `captura_estructura_carpetas.png`, `captura_pagina_panel.png`, `captura_lint_y_build.png`
