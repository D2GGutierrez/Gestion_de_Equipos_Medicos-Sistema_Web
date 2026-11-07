# Laboratorio 10 – Ejercicio 6: Contador con useState

## Qué se hizo
En `ProductoCard` se agregó el botón **"Agregar al pedido"** con `const [cantidad, setCantidad] = useState(0)`:
- El botón llama a `setCantidad(cantidad + 1)` en `onClick`.
- `{cantidad > 0 && <span>En pedido: N</span>}` → el texto solo aparece si hay al menos 1 unidad.
- `disabled={stock === 0 || cantidad >= stock}` → el botón se bloquea según un campo del registro: sin stock (Desfibrilador) o cuando ya se pidió todo el stock.
- **Contadores independientes**: cada `<ProductoCard>` es una instancia distinta y tiene su propio estado; hacer clic en uno no afecta a los demás.

## Prueba (comportamiento verificado en el navegador)
| Acción | Resultado |
|---|---|
| Estado inicial | Ningún "En pedido"; Desfibrilador (stock 0) con el botón deshabilitado |
| 2 clics en Ecógrafo (stock 3), 1 en Monitor (stock 8), 2 en Ventilador (stock 2) | Ecógrafo 2, Monitor 1, Ventilador 2 (y su botón se deshabilita: ya pidió todo el stock) |
| 1 clic más en Ecógrafo | Ecógrafo 3 y botón deshabilitado; Monitor sigue en 1 |

## ¿Por qué una variable `let` no actualiza la pantalla?
Se probó temporalmente `let cantidad = 0` con `cantidad = cantidad + 1` en el clic. En consola el valor sube (1, 2, 3) pero **la pantalla no cambia**. Motivos:
1. React solo vuelve a dibujar un componente cuando cambia su **estado** (o sus props). Cambiar una variable común no avisa a React.
2. Aunque se redibujara, la función del componente se ejecuta de nuevo desde cero y `let cantidad = 0` se reinicia; el valor no se conserva entre renderizados. `useState` sí lo conserva y, con `setCantidad`, le pide a React que redibuje.

Luego se **revirtió** la prueba; el código entregado usa `useState`.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola sin errores ni warnings.

## Capturas
- `captura_codigo_ProductoCard.jsx.png`
- `captura_antes_clics.png`, `captura_despues_clics.png`
- `captura_let_consola.png`, `captura_let_pantalla_no_cambia.png`
