# Laboratorio 11 – Ejercicio 8: Ciclo de vida con `useEffect` y verificación

## Qué se hizo
**1. Título de la pestaña – `Carrito.jsx`**
```jsx
useEffect(() => {
  document.title = `Carrito (${unidades}) — Cafetería`
  console.log('Efecto de Carrito: título actualizado, unidades =', unidades)
}, [unidades])
```
El efecto se ejecuta después de dibujar y solo cuando cambia `unidades` (el dato derivado del Ejercicio 5). Pestaña: «Carrito (0) — Cafetería» → «Carrito (1) — Cafetería» → «Carrito (2) — Cafetería».

**2. Componente `Aviso.jsx`** – muestra `Agregado: <nombre>` y desaparece a los 3 s:
```jsx
useEffect(() => {
  const temporizador = setTimeout(() => setVisible(false), 3000)
  return () => clearTimeout(temporizador)   // limpieza
}, [])
```
`Practica` guarda `{ id, nombre }` del último producto agregado y renderiza `<Aviso key={aviso.id} nombre={aviso.nombre} />`; la `key` nueva en cada alta hace que React **monte un aviso nuevo** (así el temporizador de 3 s empieza de cero con cada producto). La función que devuelve el efecto limpia el temporizador cuando el aviso se desmonta antes de tiempo (por ejemplo, al agregar otro producto antes de 3 s), para que no quede un `setTimeout` vivo apuntando a un componente que ya no existe.

## Qué ocurre con cada arreglo de dependencias (probado en el navegador)
| Acción | `[unidades]` | `[]` | sin arreglo |
|---|---|---|---|
| Al cargar la página | 2 mensajes* | 2* | 2* |
| Agregar Capuchino (unidades 0 → 1) | 1 | 0 | 1 |
| Escribir «c» en el buscador (`unidades` no cambia) | **0** | 0 | **1** |
| Agregar otro Capuchino (1 → 2) | 1 | 0 | 1 |
| Título de la pestaña al final | «Carrito (2)…» ✔ | «Carrito (0)…» ✘ (no se actualiza) | «Carrito (2)…» ✔ |

\* ver «StrictMode» más abajo.

- **`[]`**: el efecto corre **una sola vez, al montar** (y la limpieza, al desmontar). No vuelve a ejecutarse aunque cambien las unidades; por eso el título se queda en «Carrito (0)». Sirve para tareas de una sola vez, como el temporizador de `Aviso`.
- **`[unidades]`**: corre al montar y **cada vez que cambia `unidades`**. Es lo correcto para sincronizar el título con la cantidad.
- **Sin arreglo**: corre **después de cada renderizado**, aunque no haya cambiado nada relevante (escribir en el buscador volvió a ejecutarlo). Suele ser un desperdicio y puede causar bucles si el efecto cambia estado.

## ¿Por qué en desarrollo el mensaje aparece dos veces? (`React.StrictMode`)
`main.jsx` envuelve la app en `<StrictMode>`. **Solo en desarrollo**, React monta cada componente, ejecuta su limpieza y lo vuelve a montar para comprobar que los efectos se limpian bien. Por eso al cargar la página el `console.log` del efecto sale 2 veces, y al agregar el primer producto el `Aviso` registra «montado → limpiado → montado». En producción (`npm run build`) no ocurre y se ejecuta una sola vez. (Las demás ejecuciones, como el 2.º clic con «limpiado» antes de «montado», son el desmontaje real del aviso anterior.)

## `npm run lint` y `npm run build`
- `npm run lint`: **sin advertencias ni errores**, código de salida 0.
- `npm run build`: `✓ 34 modules transformed`, `✓ built in 121ms`, código de salida 0.
- Consola del navegador sin advertencias ni errores.
- Nota: en un primer intento `Aviso` recibía una función `onCerrar` y oxlint avisó `react-hooks(exhaustive-deps)` por tener `[]`; se resolvió haciendo que `Aviso` se oculte con su propio estado (`visible`), sin depender de esa función.

→ `captura_lint_y_build.png`

## Capturas
- Código: `captura_codigo_Carrito.jsx.png`, `captura_codigo_Aviso.jsx.png`, `captura_codigo_Practica.jsx.png`
- Página: `captura_01_sin_aviso.png`, `captura_02_aviso_visible.png`, `captura_03_aviso_desaparecio.png`
- Consola y pruebas: `captura_consola_aviso.png`, `captura_prueba_dependencias.png`, `captura_lint_y_build.png`
