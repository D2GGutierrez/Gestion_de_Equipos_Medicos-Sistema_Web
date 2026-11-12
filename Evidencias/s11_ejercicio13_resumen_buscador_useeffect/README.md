# Laboratorio 11 — Ejercicio 13: resumen, buscador y useEffect en el panel

Entidad del panel: **EquipoInstalado**. Todo el estado vive en `PanelEquipos` (padre); los hijos reciben datos por props y avisan con funciones.

## Componentes nuevos
- `ResumenEquipos` (hermano del listado): recibe `equipos` y calcula con `reduce` el total, los conteos por estado y el % de operativos. **No usa useState**: son datos derivados, se recalculan en cada render cuando el padre cambia el arreglo.
- `BuscadorEquipos`: input controlado (`valor`, `onCambiar`). El texto vive en `PanelEquipos`.
- `AvisoPanel`: aviso temporal con `useEffect(..., [])` y limpieza `clearTimeout`.

## Búsqueda compartida
`PanelEquipos` guarda `busqueda` y filtra por número de serie (`filter` + `includes`, sin distinguir mayúsculas) antes de pasar los equipos al listado. El resumen sigue contando **todos** los equipos; el listado muestra solo los filtrados. Si no hay coincidencias, el listado muestra «No hay equipos que coincidan con «texto»».

## useEffect
`AvisoPanel` arranca un `setTimeout` de 3 s al montarse (`[]`) y su función de limpieza lo cancela al desmontarse. El padre lo monta de nuevo con `key={aviso.id}` en cada acción, así el temporizador reinicia. Se eligió este efecto y no `document.title` para no chocar con el efecto del título del carrito de la práctica, visible en la misma página.

## Pruebas en el navegador
| Acción | Resultado |
|---|---|
| Inicial | 14 equipos · 9 operativos · 3 mantenimiento · 2 inactivos · 64 % |
| Cambiar estado ECO-0001 | 8 / 4 / 2 · 57 %; aviso «ahora MANTENIMIENTO» |
| Eliminar ECO-0001 | 13 equipos · 8 / 3 / 2 · 62 %; aviso «eliminado» |
| Buscar `MON` | 6 filas (MON-0101…0202) |
| Buscar `ZZZ-999` | «No hay equipos que coincidan con «ZZZ-999»» |
| Tras 3 s | el aviso desaparece |
| Consola | sin errores ni advertencias |

`npm run lint` y `npm run build`: código de salida 0. Sin `push` ni `splice` en los componentes del panel (solo aparecen en comentarios de otros).

## Capturas
`01_resumen_buscador`, `02_busqueda_MON`, `03_busqueda_sin_resultados`, `04_aviso`, `05_aviso_desaparecido`, `codigo_*`, `lint`, `build`.
