# Laboratorio 12 — Ejercicio 11: Alta y edición con POST y PATCH

## Qué cambió

**Django**
- `GET /api/productos/` (solo lectura, `ProductoViewSet` en `views/productos.py`, registrado en el router): el formulario necesita el nombre y los `meses_garantia` de cada producto, y esa API no existía. Se probó que es de solo lectura (POST y DELETE responden 405). Suite de pruebas: 50 OK.

**React**
- `PanelEquipos.jsx` (padre) pide equipos, productos y clientes con `Promise.all` dentro del `useEffect`, y guarda también el **equipo seleccionado** (`seleccionado`), los **errores 400** (`errores`) y si está guardando.
- `FormularioEquipo.jsx` ya no valida la serie ni agrega nada a la lista: arma el registro y lo entrega con `onGuardar(datos)`. Se llena con los datos del equipo seleccionado cuando se edita. Los mensajes de error 400 se muestran junto al formulario.
- `FilaEquipo.jsx` y `ListadoEquipos.jsx`: nuevo botón **Editar** que avisa al padre con `onEditar(id)`.

```jsx
// PanelEquipos.jsx: alta (POST) o edición (PATCH) según haya un equipo seleccionado
async function guardarEquipo(datos) {
  setGuardando(true)
  setErrores({})
  try {
    if (seleccionado) {
      const respuesta = await api.patch(`/equipos/${seleccionado.id}/`, datos)          // 200
      setEquipos(equipos.map((e) => (e.id === seleccionado.id ? respuesta.data : e)))   // map(): arreglo nuevo
      setSeleccionado(null)
    } else {
      const respuesta = await api.post('/equipos/', datos)                              // 201
      setEquipos([...equipos, respuesta.data])                                          // spread: arreglo nuevo
    }
    setVersion(version + 1)   // cambia la key del formulario y lo deja vacío
  } catch (err) {
    if (err.response && err.response.status === 400) setErrores(err.response.data)
    else setErrores({ general: ['No se pudo guardar el equipo. Intente de nuevo.'] })
  } finally {
    setGuardando(false)
  }
}
```

El botón «Poner en mantenimiento / Marcar operativo» también se conectó a la API con `PATCH {estado}` (ahora persiste en la base de datos). **Eliminar** todavía solo cambia el estado de React: se conecta a DELETE en el Ejercicio 12.

## Resultados (probados en el navegador)

| Acción | Network | Pantalla |
|---|---|---|
| Alta con serie `ABC` | **POST** `/api/equipos/` → **400** | «Número de serie: El número de serie debe tener el formato AAA-0000…» junto al formulario; la lista sigue con 14 |
| Alta con serie repetida `eco-0001` | **POST** → **400** | «Número de serie: Ya existe un equipo con ese número de serie.» |
| Alta válida `ECO-0003` | **POST** → **201 Created** (`id: 17`) | El equipo aparece sin recargar (15 equipos), el resumen sube a 10 operativos y el formulario queda vacío; garantía calculada: 2028-11-01 (+24 meses) |
| Clic en Editar | — | El formulario se llena con los datos del equipo y el botón dice «Guardar cambios» (con «Cancelar edición») |
| Guardar edición (estado → Mantenimiento) | **PATCH** `/api/equipos/17/` → **200 OK** | La fila cambia a MANTENIMIENTO y el resumen pasa a 9 operativos / 4 en mantenimiento |
| Edición con serie `XX` | **PATCH** → **400** | Mensaje de formato junto al formulario; la fila no cambia |

Los mensajes 400 son los que envía el serializer de la Semana 8/9 (`validate_numero_serie`), tal como llegan en `err.response.data`. El equipo de prueba se eliminó de la base al terminar. La consola solo muestra las líneas que el navegador imprime por cada respuesta 400; no hay advertencias de React. `npm run lint` y `npm run build` terminan con código 0.

## Capturas

- `01_antes_alta.png`, `02_despues_alta_201.png`, `03_error_400.png`, `04_formulario_edicion.png`, `05_despues_edicion_200.png` — el panel en el navegador.
- `06` a `11` — código (GET, POST/PATCH, cambiar estado, formulario, errores, botón Editar).
- `12_lint.png`, `13_build.png` — salida de `npm run lint` y `npm run build`.
- `14_network_post_201.png`, `15_network_patch_200.png`, `16_network_post_400.png`, `17_network_post_400_duplicado.png` — Network (método, código, datos enviados y recibidos).
