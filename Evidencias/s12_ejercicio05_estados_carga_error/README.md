# Laboratorio 12 — Ejercicio 5: Estados de carga y de error

## Código (`src/practica/ListaPractica.jsx`)

```jsx
const [clientes, setClientes] = useState([])
const [cargando, setCargando] = useState(true)
const [error, setError] = useState(null)

useEffect(() => {
  async function cargarClientes() {
    try {
      const respuesta = await api.get('/clientes/')
      setClientes(respuesta.data)
    } catch (err) {
      console.error('Error al pedir los clientes:', err.message)
      setError('No se pudo cargar la lista')
    } finally {
      setCargando(false)
    }
  }
  cargarClientes()
}, [])

if (cargando) return <p className="aviso">Cargando...</p>
if (error) return <p className="error">{error}</p>
if (clientes.length === 0) return <p className="vacio">No hay clientes registrados</p>
// ... lista con map() y key={c.id}
```

## Qué muestra la pantalla en cada estado

| Estado | Cuándo ocurre | Pantalla |
|---|---|---|
| Cargando | Desde que el componente aparece hasta que llega la respuesta (o falla) | «Cargando...» |
| Error | Django apagado, red caída o `timeout` de 5 s | «No se pudo cargar la lista» (y en la consola: `Error al pedir los clientes: Network Error`, `net::ERR_CONNECTION_REFUSED`) |
| Lista vacía | La API responde 200 con `[]` | «No hay clientes registrados» |
| Con datos | La API responde 200 con registros | Lista de clientes |

Pruebas hechas en el navegador: el estado de carga se vio con una respuesta demorada 2,5 s; el error, con Django apagado; la lista vacía, interceptando la respuesta para que devolviera `[]`; y los datos, con Django encendido (3 clientes). Con datos y en la carga normal la consola queda sin errores ni advertencias. `npm run lint` y `npm run build` terminan con código 0. En desarrollo el mensaje de error se imprime dos veces por `React.StrictMode`.

## Por qué no dejar la pantalla en blanco

Mientras llega la respuesta, la lista está vacía y, si falla, seguiría vacía: el usuario no sabría si la aplicación se rompió, si todavía carga o si de verdad no hay datos. Los tres mensajes le dicen qué está pasando y qué esperar. `finally` garantiza que `cargando` pase a `false` tanto si la petición funcionó como si falló; sin él, un error dejaría «Cargando...» para siempre.

## Capturas

- `01_estado_cargando.png`, `02_estado_error.png`, `03_estado_vacio.png`, `04_estado_con_datos.png` — los estados en el navegador.
- `05_codigo_ListaPractica.png` — código.
- `06_consola_error.png` — mensajes de la consola con Django apagado.
