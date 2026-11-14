# Laboratorio 12 — Ejercicio 10: Cargar el listado del panel desde la API

## Qué cambió (`src/components/PanelEquipos.jsx`)

Los 14 equipos escritos a mano (`equiposIniciales`, Semana 11) se reemplazaron por un GET a la API dentro de un `useEffect`, usando la instancia `api` de `src/api.js`. El componente padre guarda los registros y los estados de la petición, y entrega los datos a los hijos por props.

```jsx
const [equipos, setEquipos] = useState([])
const [cargando, setCargando] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  async function cargarEquipos() {
    try {
      const respuesta = await api.get('/equipos/')      // GET http://127.0.0.1:8000/api/equipos/
      setEquipos(respuesta.data)
    } catch (err) {
      console.error('Error al pedir los equipos:', err.message)
      setError('No se pudo cargar la lista de equipos')
    } finally {
      setCargando(false)
    }
  }
  cargarEquipos()
}, [])

if (cargando) return <p className="aviso">Cargando equipos...</p>
if (error) return <p className="error">{error}</p>
// ... <ResumenEquipos equipos={equipos} /> y <ListadoEquipos equipos={equiposFiltrados} ... />
```

## Resultados (probados en el navegador)

| Caso | Cómo se probó | Pantalla |
|---|---|---|
| Cargando | Respuesta demorada 1,5 s | «Cargando equipos...» |
| Con datos | Django encendido | 14 equipos; resumen: 14 equipos · 9 operativos · 3 en mantenimiento · 2 inactivos · 64 % |
| Error | Petición rechazada (como con Django apagado) | «No se pudo cargar la lista de equipos»; consola: `Error al pedir los equipos: Network Error` |
| Lista vacía | La API responde `[]` | «No hay equipos registrados» |

Network: **GET** `http://127.0.0.1:8000/api/equipos/` → **200 OK** (`application/json`). En desarrollo se ven dos peticiones por `React.StrictMode`. Con datos, la consola queda sin errores ni advertencias; `npm run lint` y `npm run build` terminan con código 0.

## Función adaptadora

El enunciado pide convertir los decimales que la API entregue como texto. `EquipoInstalado` no tiene campos decimales (solo texto, fechas `AAAA-MM-DD` y claves foráneas), y los nombres de los campos ya coinciden con los que usan los componentes, así que no hace falta una función adaptadora en esta entidad.

## Estado actual del panel

El listado, el resumen y el buscador ya trabajan con datos reales. El alta, el cambio de estado y la eliminación todavía actualizan solo el estado de React (no persisten en la base de datos): se conectan a la API en los Ejercicios 11 y 12. El formulario sigue usando las listas de productos y clientes escritas a mano hasta el Ejercicio 11.

## Capturas

- `01_cargando.png`, `02_listado_desde_api.png`, `03_error.png`, `04_vacio.png` — los estados en el navegador.
- `05_codigo_imports.png`, `06_codigo_estado_y_useeffect.png`, `07_codigo_estados_render.png` — código.
- `08_lint.png`, `09_build.png` — salida de `npm run lint` y `npm run build`.
- `10_network_get_200.png` — petición GET con código 200.
