# Laboratorio 12 — Ejercicio 13: Búsqueda, filtros y resumen con datos de la API

## Qué cambió

- `BuscadorEquipos.jsx` (campo controlado) y el nuevo `FiltroEstado.jsx` (select controlado por estado) avisan al padre con `onCambiar`.
- `PanelEquipos.jsx` guarda `busqueda` y `filtroEstado` y **ya no filtra en el navegador**: envía los valores como parámetros a la API (`?search=` y `?estado=`) y recarga el listado cuando cambian. Solo se envían los parámetros con valor.
- El catálogo (productos y clientes) se pide una sola vez; el listado de equipos tiene su propio `useEffect` con `[busqueda, filtroEstado]`, y sus propios estados de carga y error para que el campo de búsqueda no se desmonte ni pierda el foco mientras se escribe.
- **Opcional hecho:** `AbortController` en la limpieza del efecto: si el usuario sigue escribiendo, la petición pendiente se cancela y solo vale la última.
- `ResumenEquipos` no cambió: sigue calculando con `reduce` sobre los equipos que recibe, que ahora son los que devolvió la API, así que el resumen refleja el resultado de la búsqueda o el filtro.

```jsx
useEffect(() => {
  const controlador = new AbortController()
  async function cargarEquipos() {
    setCargandoLista(true)
    setErrorLista(null)
    const params = {}
    if (busqueda.trim() !== '') params.search = busqueda.trim()
    if (filtroEstado !== '') params.estado = filtroEstado
    try {
      const respuesta = await api.get('/equipos/', { params, signal: controlador.signal })
      setEquipos(respuesta.data)
    } catch (err) {
      if (err.code === 'ERR_CANCELED') return
      setErrorLista('No se pudo cargar la lista de equipos')
    } finally {
      if (!controlador.signal.aborted) setCargandoLista(false)
    }
  }
  cargarEquipos()
  return () => controlador.abort()
}, [busqueda, filtroEstado])
```

## URLs generadas y resultados (probados en el navegador)

| Acción | URL generada por Axios | Código | Resultado | Resumen mostrado |
|---|---|---|---|---|
| Al abrir el panel | `/api/equipos/` | 200 | 14 equipos | 14 · 9 operativos · 3 mantenimiento · 2 inactivos · 64 % |
| Buscar `MON` | `/api/equipos/?search=MON` | 200 | 6 equipos | 6 · 4 · 1 · 1 · 67 % |
| Buscar `MON` y filtrar `Operativo` | **`/api/equipos/?search=MON&estado=OPERATIVO`** (parámetros combinados con `&`) | 200 | 4 equipos | 4 · 4 · 0 · 0 · 100 % |
| Solo filtrar `En mantenimiento` | `/api/equipos/?estado=MANTENIMIENTO` | 200 | 3 equipos | 3 · 0 · 3 · 0 · 0 % |
| Buscar `ZZZ` con `En mantenimiento` | `/api/equipos/?search=ZZZ&estado=MANTENIMIENTO` | 200 | 0 equipos | «No hay equipos que coincidan con «ZZZ + estado MANTENIMIENTO»» |

Cancelación (respuestas demoradas 0,7 s y escribiendo `MON` letra por letra): las peticiones de `?search=M` y `?search=MO` quedan **canceladas** (`net::ERR_ABORTED`) y la lista final corresponde a `?search=MON` (6 equipos). La consola quedó sin errores ni advertencias, y `npm run lint` y `npm run build` terminan con código 0.

## Notas

- La búsqueda ahora la hace el servidor y cubre número de serie, nombre del producto y razón social del cliente (antes solo filtraba por serie en el navegador).
- Si se da de alta o se cambia el estado de un equipo mientras hay un filtro activo, la fila sigue la respuesta de la API (se actualiza la lista actual); al cambiar el filtro, el listado se vuelve a pedir y queda consistente.

## Capturas

- `01_sin_filtros.png`, `02_busqueda_MON.png`, `03_busqueda_y_estado.png`, `04_solo_estado.png`, `05_sin_resultados.png` — el panel en el navegador.
- `06` a `09` — código (useEffect con parámetros, render, FiltroEstado, resumen).
- `10_lint.png`, `11_build.png` — salida de `npm run lint` y `npm run build`.
- `12_network_urls.png` — URLs generadas, métodos y códigos.
