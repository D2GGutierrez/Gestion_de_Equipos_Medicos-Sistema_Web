# Laboratorio 11 – Ejercicio 2: Reconocer los tipos de props

## Tabla de props del Ejercicio 1
| Nombre de la prop | Tipo de valor | Qué componente la define (la envía) | Qué componente la lee |
|---|---|---|---|
| `productos` | arreglo (de objetos) | `Practica` → `<Catalogo productos={productos} />` | `Catalogo` |
| `producto` | objeto | `Catalogo` → `<ProductoCard producto={p} />` | `ProductoCard` |

(`key={p.id}` no cuenta como prop: React la usa internamente para identificar cada elemento de la lista y el componente hijo no puede leerla.)
Todavía no hay props de tipo función; aparecen en el Ejercicio 3 con `onAgregar`.

## ¿Por qué `ProductoCard` no puede modificar la prop `producto`?
Las props pertenecen al componente que las envía: el dato vive en `Practica` y `ProductoCard` solo recibe una referencia para mostrarlo. Si el hijo lo cambiara, el padre y los demás componentes verían datos distintos sin que React se entere y la pantalla dejaría de ser predecible. Si algo debe cambiar, lo hace el dueño del dato (el padre) con su estado, y el hijo lo recibe de nuevo por props.

### Pruebas realizadas (temporales, ya revertidas)
- **Prueba A – reasignar la prop** (`props.producto = {...}`): el navegador lanzó `Cannot assign to read only property 'producto' of object '#<Object>'` y la pantalla quedó en blanco. React congela el objeto `props`.
  → `captura_prueba_A_reasignar_prop_error.png`
- **Prueba B – cambiar una propiedad del objeto** (`producto.nombre = producto.nombre.toUpperCase() + '!'`): aquí **no hay error**, porque JavaScript sí permite modificar por dentro el objeto recibido. Pero el resultado es un bug: se modificó el dato original compartido y el nombre apareció como `CAFÉ AMERICANO!!` (con dos signos porque en desarrollo `React.StrictMode` ejecuta el render dos veces y la mutación se aplicó dos veces). Por eso la regla es una convención que hay que respetar: no mutar props, ni la prop ni lo que tiene dentro.
  → `captura_prueba_B_mutar_objeto.png`

El código entregado de `ProductoCard.jsx` solo lee `producto`; no lo modifica.

## Equivalente en los Templates de Django
El **context** que una View entrega al template (`render(request, 'lista.html', {'productos': productos})`) cumple un papel parecido: la vista es dueña de los datos y el template solo los muestra con `{{ producto.nombre }}`; el template no puede cambiar lo que la vista le dio. Así como el context baja de la View al Template, las props bajan del padre al hijo. La diferencia es que en React, cuando el padre cambia su estado, vuelve a entregar las props nuevas y la pantalla se redibuja sola, mientras que un template de Django se genera una vez por petición.

## Capturas
`captura_tabla_de_props.png`, `captura_prueba_A_reasignar_prop_error.png`, `captura_prueba_B_mutar_objeto.png`
