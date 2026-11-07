# Laboratorio 10 – Ejercicio 2: Crear el primer componente funcional

## El componente (`src/components/ProductoCard.jsx`)
```jsx
import { productos } from '../datos.js'

function ProductoCard() {
  const p = productos[0]            // por ahora siempre el primer producto (en el ejercicio 3 llegará por props)
  return (
    <div className="tarjeta">
      <strong>{p.nombre}</strong> — {p.marca} {p.modelo} · {p.categoria.nombre} ·
      S/ {Number(p.precio_base).toFixed(2)} · Stock: {p.stock}
    </div>
  )
}

export default ProductoCard
```
- Es una función normal de JavaScript que devuelve JSX.
- Su nombre empieza con **mayúscula** (`ProductoCard`) y el archivo tiene el mismo nombre.
- `export default` permite importarlo desde otro archivo.

## Uso en `App.jsx`
```jsx
import ProductoCard from './components/ProductoCard.jsx'
...
<ProductoCard />
<ProductoCard />
```
Resultado (`captura_pagina_mayuscula.png`): la tarjeta del Ecógrafo Doppler Color aparece **dos veces**. Se escribe el componente una vez y se usa tantas veces como se necesite, como una etiqueta propia. En la consola no aparece ninguna advertencia. `npm run lint` sin avisos y `npm run build` correcto.

## ¿Qué ocurre si el nombre del componente se escribe en minúscula?
Se probó cambiando `<ProductoCard />` por `<productoCard />` (capturas `captura_pagina_minuscula.png` y `captura_consola_minuscula.png`):
- **La tarjeta desaparece**: la página muestra el título y la sección, pero ninguna de las dos tarjetas.
- **La consola muestra errores**: `<productoCard /> is using incorrect casing. Use PascalCase for React components, or lowercase for HTML elements` y `The tag <productoCard> is unrecognized in this browser. If you meant to render a React component, start its name with an uppercase letter`.

La explicación es que React usa la primera letra para saber de qué se trata. Si empieza con minúscula (`<div>`, `<p>`, `<li>`) cree que es una etiqueta de HTML normal; si empieza con mayúscula, sabe que es un componente suyo y ejecuta la función. Con `productoCard` en minúscula, React no busca la función: crea una etiqueta HTML llamada `productocard` que el navegador no conoce, vacía y sin contenido, y por eso no se ve nada. El `import` queda sin usarse. Lo engañoso es que la página no se rompe, simplemente no aparece el componente; por eso conviene mirar la consola. Se volvió a poner `<ProductoCard />` después de la prueba.

Equivalente en Django: es como llamar a un `{% include 'producto_card.html' %}` con el nombre mal escrito, pero aquí el error no detiene la página, solo se ve en la consola.

## Nota
La carpeta `src/components/` conserva el `.gitkeep` del ejercicio 1; ya no es necesario (la carpeta tiene un archivo) y se puede borrar cuando quieras.
