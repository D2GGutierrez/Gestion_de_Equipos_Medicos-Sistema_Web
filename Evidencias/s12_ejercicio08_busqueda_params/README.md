# Laboratorio 12 — Ejercicio 8: Parámetros de búsqueda y verificación

## Django: `?search=` en la API de clientes

`ClienteViewSet` no tenía búsqueda, así que se agregó (como ya la tenía `CategoriaViewSet`):

```python
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all().order_by('id')
    serializer_class = ClienteSerializer

    filter_backends = [filters.SearchFilter]
    search_fields = ['razon_social', 'numero_identificacion']
```

## React: campo controlado + useEffect con `[buscar]`

```jsx
const [buscar, setBuscar] = useState('')

useEffect(() => {
  let vigente = true
  async function cargarClientes() {
    setCargando(true)
    setError(null)
    try {
      const respuesta = await api.get('/clientes/', { params: { search: buscar } })
      if (vigente) setClientes(respuesta.data)
    } catch (err) { /* ... */ } finally { if (vigente) setCargando(false) }
  }
  cargarClientes()
  return () => { vigente = false }   // ignora respuestas viejas si el texto cambió
}, [buscar])

<input className="buscador" value={buscar} onChange={(e) => setBuscar(e.target.value)} />
```

`[buscar]` hace que el efecto se ejecute de nuevo cada vez que cambia el texto. La función de limpieza evita que una respuesta lenta de una búsqueda anterior pise a la más reciente.

## Resultados (probados en el navegador)

| Texto | URL generada por Axios | Código | Resultado |
|---|---|---|---|
| (vacío) | `/api/clientes/?search=` | 200 | 3 clientes |
| `san` | `/api/clientes/?search=san` | 200 | 2: Clínica San Gabriel, Centro Médico Santa Rosa |
| `zzz` | `/api/clientes/?search=zzz` | 200 | lista vacía → «No hay clientes que coincidan con «zzz»» |

Nota: la búsqueda no ignora tildes (en SQLite, «clinica» no encuentra «Clínica»); distingue acentos pero no mayúsculas. La consola quedó sin errores ni advertencias. Las 38 pruebas de Django (`manage.py test inventario`) siguen pasando.

## Verificación

`npm run lint` y `npm run build` terminan con código de salida 0 (capturas 07 y 08).

## Recorrido de una petición

- **React** guarda el estado (`buscar`, `clientes`, `cargando`, `error`), decide cuándo pedir datos (`useEffect`) y dibuja la pantalla con lo que llega.
- **Axios** (`api.js`) arma la petición HTTP: une la `baseURL` con la ruta, convierte `params` en `?search=...`, envía el JSON y devuelve la respuesta ya convertida (`respuesta.data`) o lanza un error si el código no es 2xx.
- **El ViewSet** recibe la petición ya enrutada (`/api/clientes/`), decide qué operación corresponde al método HTTP y aplica el filtro de búsqueda.
- **El serializer** convierte los objetos de Python a JSON (y viceversa) y valida los datos que llegan (`validate_numero_identificacion`).
- **El ORM** traduce la consulta a SQL (`WHERE razon_social LIKE ... OR numero_identificacion LIKE ...`) y lee o escribe en SQLite.

## Por qué la API todavía está abierta a cualquier persona

La API no tiene **autenticación ni permisos**: no pide usuario, contraseña ni token, y Django REST Framework, sin configuración, permite todo a todos. Cualquiera que conozca la URL (con un navegador, `curl` o Postman) puede listar, crear, modificar o eliminar clientes. CORS no lo evita: solo le dice al **navegador** qué páginas pueden leer las respuestas; un programa fuera del navegador ignora CORS. Falta agregar autenticación (por ejemplo, tokens o JWT) y permisos por rol.

## Capturas

- `01_sin_busqueda.png`, `02_busqueda_san.png`, `03_busqueda_sin_resultados.png` — la página.
- `04_codigo_useeffect_buscar.png`, `05_codigo_input_buscador.png`, `06_codigo_django_search.png` — código.
- `07_lint.png`, `08_build.png` — salida de `npm run lint` y `npm run build`.
- `09_network_search.png` — URLs generadas con `?search=` (pestaña Network).
