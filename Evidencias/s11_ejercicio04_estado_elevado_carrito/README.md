# Laboratorio 11 – Ejercicio 4: Elevar el estado, un carrito compartido

## Qué se hizo
- **`Practica.jsx` (padre)** guarda el carrito: `const [carrito, setCarrito] = useState([])`, un arreglo de líneas `{ id, nombre, precio, cantidad }`.
- **`agregarAlCarrito(producto)`** (la función que baja hasta `ProductoCard` como `onAgregar`):
  - si el producto **ya está** en el carrito: `setCarrito(carrito.map(...))`, que devuelve un arreglo nuevo con la `cantidad` de esa línea aumentada en 1 (`{ ...l, cantidad: l.cantidad + 1 }`);
  - si **no está**: `setCarrito([...carrito, { id, nombre, precio, cantidad: 1 }])`, un arreglo nuevo con spread. No se usa `push` en ninguna parte.
- **`Carrito.jsx`** es **hermano** de `Catalogo`: recibe `lineas` por props y las muestra con `map()` y `key={l.id}`; no guarda nada.

Flujo: el clic en un botón de `ProductoCard` sube por `onAgregar` hasta `Practica`, que actualiza el estado, y el carrito nuevo baja por props a `Carrito`; React vuelve a dibujar.

## Prueba
| Acción | Carrito |
|---|---|
| Inicio | (vacío) |
| 1 clic en Capuchino | Capuchino × 1 |
| 2.º clic en Capuchino, 1 en Café americano, 1 en Tostada | Capuchino × 2, Café americano × 1, Tostada × 1 |

Al repetir un producto no se crea una línea nueva: aumenta su cantidad.

## ¿Por qué el carrito no puede guardarse dentro de `ProductoCard` ni de `Catalogo`?
- **En `ProductoCard`:** hay una instancia por producto y cada una tendría su propio estado, separado de las demás; ninguna sabría qué agregaron las otras. Además `Carrito` no es su padre: en React los datos solo bajan por props, así que `Carrito` no puede leer el estado de un componente que no está por encima de él.
- **En `Catalogo`:** `Carrito` es su **hermano**, no su hijo. Un hermano no puede leer el estado de otro hermano. El carrito lo necesitan `Catalogo` (para avisar de lo que se agrega) y `Carrito` (para mostrarlo), así que debe vivir en el **ancestro común más cercano**: `Practica`. Eso es "elevar el estado".

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola del navegador sin errores ni warnings.

## Capturas
`captura_codigo_Practica.jsx.png`, `captura_codigo_Carrito.jsx.png`, `captura_01_carrito_vacio.png`, `captura_02_carrito_con_lineas.png`
