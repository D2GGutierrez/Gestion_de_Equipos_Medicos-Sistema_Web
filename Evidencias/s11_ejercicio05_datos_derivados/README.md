# Laboratorio 11 – Ejercicio 5: Calcular datos derivados

## Qué se hizo
En `Carrito.jsx` se calculan, **en cada renderizado y a partir de las props `lineas`**, dos datos derivados con `reduce()`:

```jsx
const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)
```

y se muestran como `Unidades: N · Total: S/ X.XX` (con `toFixed(2)`). El precio llega como texto (igual que la API), por eso se convierte con `Number(...)`. No se creó ningún `useState` nuevo.

## Prueba
| Acción | Unidades | Total |
|---|---|---|
| Carrito vacío | 0 | S/ 0.00 |
| 1 Capuchino | 1 | S/ 9.00 |
| **2 Capuchinos + 1 Café americano** | **3** | **S/ 24.50** (2 × 9.00 + 6.50) |
| + 1 Torta de chocolate (extra) | 4 | S/ 35.00 |

## ¿Por qué el total no necesita su propio `useState`?
Porque el total no es un dato nuevo, sino una consecuencia de datos que ya existen: siempre se puede obtener a partir de las líneas del carrito. Si se guardara en su propio estado habría dos fuentes de verdad (las líneas y el total) que habría que mantener sincronizadas a mano, y bastaría olvidarse de actualizar una para que la pantalla mostrara un total incorrecto. Calculado en cada renderizado, el total siempre coincide con el carrito: cuando el padre cambia las líneas, `Carrito` se vuelve a dibujar y el cálculo se rehace solo. La regla: guardar en el estado lo mínimo y calcular el resto.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola del navegador sin errores ni warnings.

## Capturas
`captura_codigo_Carrito.jsx.png`, `captura_01_carrito_vacio.png`, `captura_02_total_24_50.png`
