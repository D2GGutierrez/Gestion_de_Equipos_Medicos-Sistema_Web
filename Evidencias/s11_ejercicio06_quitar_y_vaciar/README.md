# Laboratorio 11 – Ejercicio 6: Quitar y vaciar desde el hijo

## Qué se hizo
- **`Carrito.jsx`** (hijo) recibe dos funciones más por props, `onQuitar` y `onVaciar`, y **no modifica la lista él mismo**: solo avisa.
  - Cada línea tiene un botón **Quitar**: `onClick={() => onQuitar(l.id)}`.
  - Debajo del total hay un botón **Vaciar carrito**: `onClick={onVaciar}` (se muestra solo si hay líneas).
  - `{lineas.length === 0 && <p>El carrito está vacío</p>}` muestra el mensaje con `&&` cuando no hay líneas.
- **`Practica.jsx`** (padre) es quien actualiza el estado:
  - `quitarDelCarrito(id)` → `setCarrito(carrito.filter((l) => l.id !== id))`: `filter()` devuelve un arreglo **nuevo** sin esa línea.
  - `vaciarCarrito()` → `setCarrito([])`: reemplaza el estado por un arreglo vacío nuevo.

Flujo: clic en **Quitar** → `onQuitar(id)` (función recibida por props) → `Practica` actualiza el estado → el carrito nuevo baja por props a `Carrito`, que se vuelve a dibujar con el total recalculado.

## Prueba
| Paso | Carrito | Unidades · Total |
|---|---|---|
| Inicio | «El carrito está vacío» | 0 · S/ 0.00 |
| 2 Capuchinos + 1 Café americano + 1 Tostada | Capuchino × 2, Café americano × 1, Tostada × 1 | 4 · S/ 29.00 |
| **Quitar** Café americano | Capuchino × 2, Tostada × 1 | 3 · S/ 22.50 |
| **Vaciar carrito** | «El carrito está vacío» (el botón Vaciar desaparece) | 0 · S/ 0.00 |

## Verificación de que no se usa `push` ni `splice`
`grep -nE "\.push\(|\.splice\(" src/practica/*.jsx` no devuelve ningún resultado: el estado solo se actualiza con arreglos nuevos (`[...]`, `map`, `filter`, `[]`).

## Otras verificaciones
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola del navegador sin errores ni warnings.
- Los botones rojos usan una clase propia (`.boton-quitar`) para no cambiar el estilo de los botones de ejercicios anteriores.

## Capturas
`captura_codigo_Practica.jsx.png`, `captura_codigo_Carrito.jsx.png`, `captura_sin_push_ni_splice.png`, `captura_01_carrito_vacio.png`, `captura_02_antes_de_quitar.png`, `captura_03_despues_de_quitar.png`, `captura_04_despues_de_vaciar.png`
