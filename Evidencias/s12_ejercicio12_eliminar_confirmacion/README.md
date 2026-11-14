# Laboratorio 12 — Ejercicio 12: Eliminar con confirmación

## Qué cambió

- `FilaEquipo.jsx`: el botón **Eliminar** ya no elimina: muestra «¿Eliminar TST-0001? Esta acción no se puede deshacer.» con los botones **Confirmar** y **Cancelar** (confirmación con un segundo clic; el paso es solo de pantalla y vive en la fila con `useState`). Solo al confirmar se avisa al padre con `onEliminar(id)`.
- `PanelEquipos.jsx`: `eliminarEquipo` ahora es una petición DELETE a la API:

```jsx
async function eliminarEquipo(id) {
  const equipo = equipos.find((e) => e.id === id)
  try {
    await api.delete(`/equipos/${id}/`)                 // 204 No Content
    setEquipos(equipos.filter((e) => e.id !== id))      // filter(): arreglo nuevo sin el equipo
    avisar(`Equipo ${equipo.numero_serie} eliminado`)
  } catch (err) {
    if (err.response && err.response.status === 404) {
      setEquipos(equipos.filter((e) => e.id !== id))    // ya no existe en el servidor: se pone al día la lista
      avisar(`El equipo ${equipo.numero_serie} ya no existe en el servidor (404). Se quitó de la lista.`, 'error')
    } else {
      avisar(`No se pudo eliminar el equipo ${equipo.numero_serie}`, 'error')
    }
  }
}
```

- `AvisoPanel.jsx`: nueva prop `tipo` para mostrar el aviso en rojo cuando algo falla.

## Resultados (probados en el navegador)

Se crearon dos equipos de prueba (`TST-0001` y `TST-0002`) y se eliminaron al terminar; la base volvió a tener los 14 equipos originales.

| Prueba | Network | Pantalla |
|---|---|---|
| Primer clic en Eliminar | (ninguna petición) | Aparece la pregunta de confirmación con Confirmar / Cancelar |
| Cancelar | (ninguna petición) | La fila vuelve a sus botones; siguen 16 equipos |
| Confirmar | **DELETE** `/api/equipos/20/` → **204 No Content** | La fila desaparece (16 → 15), el resumen se actualiza (10 operativos, 67 %) y aviso «Equipo TST-0001 eliminado» |
| Confirmar un equipo que otra persona ya había borrado | **DELETE** `/api/equipos/21/` → **404 Not Found** (`No EquipoInstalado matches the given query.`) | Aviso en rojo «El equipo TST-0002 ya no existe en el servidor (404). Se quitó de la lista.»; la fila se quita (15 → 14) |

Para provocar el 404 se borró `TST-0002` directamente en el servidor mientras la pantalla todavía lo mostraba. La consola solo muestra la línea que el navegador imprime por la respuesta 404; no hay advertencias de React. `npm run lint` y `npm run build` terminan con código 0.

## Por qué se confirma antes de eliminar

DELETE es irreversible: el registro desaparece de la base de datos. La confirmación evita borrados por un clic accidental. Y el estado de React solo cambia cuando el servidor responde (204 o 404), de modo que la pantalla nunca muestra algo que no coincide con la base de datos.

## Capturas

- `01_fila_antes.png`, `02_confirmacion.png`, `03_despues_204.png`, `04_mensaje_404.png` — el panel en el navegador.
- `05` a `07` — código (eliminarEquipo, confirmación en la fila, AvisoPanel).
- `08_lint.png`, `09_build.png` — salida de `npm run lint` y `npm run build`.
- `10_network_delete_204.png`, `11_network_delete_404.png` — Network (método y código).
