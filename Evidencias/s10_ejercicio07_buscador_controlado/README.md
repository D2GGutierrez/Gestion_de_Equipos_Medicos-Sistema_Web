# Laboratorio 10 – Ejercicio 7: Buscador controlado

## Qué se hizo
En `ListaProductos` (el componente que dibuja la lista, por eso el estado vive ahí):
- `const [busqueda, setBusqueda] = useState('')` guarda el texto escrito.
- `<input value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />` es un **input controlado**: lo que se ve en el campo siempre es el valor del estado.
- `productos.filter((p) => p.nombre.toLowerCase().includes(texto))` calcula la lista filtrada en cada renderizado, con `toLowerCase()` a ambos lados (no distingue mayúsculas). **No se modifica el arreglo original**; el filtro devuelve uno nuevo.
- El título muestra la cantidad filtrada: `Productos (N)`.
- Mensajes con `&&`: "No hay registros" si no hay datos, y `Sin resultados para «texto»` si la búsqueda no encuentra nada.

## Búsquedas documentadas
| Búsqueda | Resultado |
|---|---|
| (vacío) | 5 productos |
| `MONITOR` (mayúsculas) | 1: Monitor de Signos Vitales (prueba que no distingue mayúsculas) |
| `eC` (mayúsculas y minúsculas mezcladas) | 2: Ecógrafo Doppler Color y Ventilador Mecánico |
| `zzz` | 0 productos y el mensaje «Sin resultados para «zzz»» |
| se borra el texto | vuelven los 5 productos |

## Detalle a tener en cuenta
Al filtrar, las tarjetas que salen de la lista se desmontan y **pierden su contador** del Ejercicio 6 (su estado vive en cada `ProductoCard`). Las que siguen visibles lo conservan gracias a la `key={p.id}`.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola sin errores ni warnings.

## Capturas
- `captura_codigo_ListaProductos.jsx.png`
- `captura_00_sin_busqueda.png`, `captura_01_busqueda_MONITOR.png`, `captura_02_busqueda_eC.png`, `captura_03_busqueda_zzz.png`
