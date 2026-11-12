# Laboratorio 11 – Ejercicio 3: Enlazar un evento con una función del padre

## Qué se hizo
| Archivo | Cambio |
|---|---|
| `Practica.jsx` | Define `agregarAlCarrito(producto)` (por ahora solo `console.log('Agregar al carrito:', producto.nombre)`) y la pasa a `Catalogo` con `onAgregar={agregarAlCarrito}` |
| `Catalogo.jsx` | Recibe `onAgregar` y la pasa a cada `ProductoCard` |
| `ProductoCard.jsx` | Botón **Agregar** con `onClick={() => onAgregar(producto)}` y `disabled={producto.stock === 0}` |

Los datos bajan por props (`productos` → `producto`) y el aviso sube por una función (`onAgregar`): el hijo no sabe qué hace el padre con el aviso, solo lo llama y le entrega el producto.

## Comprobación en la consola
- Al cargar la página no hay mensajes. Al hacer clic en Capuchino, Café americano y Torta de chocolate aparece `Agregar al carrito: <nombre>`, uno por clic.
- El botón del Jugo de naranja (stock 0) está desactivado.
→ `captura_consola_correcta.png`, `captura_pagina.png`

## Prueba del error: `onClick={onAgregar(producto)}` (temporal, ya revertida)
**Por qué ocurre:** con paréntesis, `onAgregar(producto)` **se ejecuta en ese instante**, mientras React dibuja el botón, y lo que se le entrega a `onClick` es su resultado (`undefined`), no la función. La regla: `onClick` necesita recibir una *función*, no el *resultado de llamarla*.

- **Prueba A** (con la función solo con `console.log`): en este caso no hay error rojo, pero sí el comportamiento equivocado: al cargar la página, sin hacer clic, aparecen **10 mensajes** (5 productos × 2 renders de `React.StrictMode`) y al hacer clic **no pasa nada**. → `captura_prueba_A_consola.png`
- **Prueba B** (el padre además cambia un estado con `setState`, como hará en el Ejercicio 4): ahora sí aparece el error rojo `Cannot update a component (Practica) while rendering a different component (ProductoCard)`: el hijo intentó actualizar el estado del padre mientras se dibujaba. → `captura_prueba_B_error.png`

**Cómo se corrige:** envolver la llamada en una función flecha, `onClick={() => onAgregar(producto)}`, que React guarda y ejecuta solo cuando el usuario hace clic. (Si no hubiera que enviar el producto, bastaría `onClick={onAgregar}`, sin paréntesis.) El código entregado usa la forma correcta.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente.

## Capturas
`captura_codigo_Practica.jsx.png`, `captura_codigo_Catalogo.jsx.png`, `captura_codigo_ProductoCard.jsx.png`, `captura_pagina.png`, `captura_consola_correcta.png`, `captura_prueba_A_consola.png`, `captura_prueba_B_error.png`
