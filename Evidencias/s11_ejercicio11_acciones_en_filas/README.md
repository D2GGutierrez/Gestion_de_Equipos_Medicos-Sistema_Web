# Laboratorio 11 – Ejercicio 11: Eventos enlazados en el listado

## Qué se hizo
Cada fila del panel tiene **dos botones de acción** que avisan al padre con funciones recibidas por props:

| Archivo | Cambio |
|---|---|
| `FilaEquipo.jsx` | Botón de estado: `onClick={() => onCambiarEstado(equipo.id)}` (texto «Poner en mantenimiento» si está operativo, «Marcar operativo» en otro caso) y botón **Eliminar**: `onClick={() => onEliminar(equipo.id)}` |
| `ListadoEquipos.jsx` | Recibe `onEliminar` y `onCambiarEstado` y las pasa a cada `FilaEquipo` |
| `PanelEquipos.jsx` (padre) | Define las dos funciones que cambian el estado |

```jsx
// Eliminar: filter() devuelve un arreglo NUEVO sin ese equipo
function eliminarEquipo(id) { setEquipos(equipos.filter((e) => e.id !== id)) }

// Cambiar estado: map() devuelve un arreglo NUEVO; solo ese equipo se copia con otro estado
function cambiarEstado(id) {
  setEquipos(equipos.map((e) =>
    e.id === id ? { ...e, estado: e.estado === 'OPERATIVO' ? 'MANTENIMIENTO' : 'OPERATIVO' } : e))
}
```
No se usa `push` ni `splice` en ningún lugar (`captura_sin_push_ni_splice.png`).

## Lista antes y después de cada acción
| Acción | Antes | Después |
|---|---|---|
| Estado inicial | 14 equipos; ECO-0001 `OPERATIVO`, MON-0103 `MANTENIMIENTO` | — |
| **Cambiar estado** de ECO-0001 | `OPERATIVO`, botón «Poner en mantenimiento» | `MANTENIMIENTO`, botón «Marcar operativo»; sigue habiendo 14 |
| **Cambiar estado** de MON-0103 | `MANTENIMIENTO` | `OPERATIVO`; sigue habiendo 14 |
| **Eliminar** OXI-0401 | 14 equipos, la fila OXI-0401 existe | `Equipos instalados (13)`, la fila ya no existe |

## ¿Por qué la fila no modifica la lista por sí misma?
`FilaEquipo` solo recibe **su propio equipo** (`equipo`); no tiene el arreglo completo, que es del padre. Aunque lo tuviera, en React los datos bajan por props y no se modifican desde el hijo: si la fila cambiara algo por su cuenta, React no se enteraría (solo se redibuja cuando cambia el estado con `setEquipos`) y el listado, el resumen y el buscador, que dependen del mismo arreglo, quedarían desincronizados. Por eso la fila solo **avisa** («quiero eliminar el equipo 13») y el dueño del estado, `PanelEquipos`, es quien crea el arreglo nuevo con `filter()` o `map()` y se lo devuelve a todos por props.

## Verificación
- `npm run lint`: sin advertencias ni errores (código 0). `npm run build`: compila (código 0). Consola del navegador sin errores ni warnings.

## Capturas
`captura_codigo_PanelEquipos.jsx.png`, `captura_codigo_ListadoEquipos.jsx.png`, `captura_codigo_FilaEquipo.jsx.png`, `captura_sin_push_ni_splice.png`, `captura_01_antes.png`, `captura_02_despues_cambiar_estado.png`, `captura_03_despues_eliminar.png`
