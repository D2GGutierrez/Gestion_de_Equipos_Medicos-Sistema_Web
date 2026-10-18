# Ejercicio 6 – Renderizado condicional

Se amplió `src/App.jsx` (completo en `App.jsx`, captura en `captura_codigo_App.jsx.png`):

```jsx
{/* && : solo aparece si el arreglo está vacío */}
{productos.length === 0 && <p>No hay registros</p>}

<li key={p.id}>
  ...
  {/* ternario: una cosa u otra según el stock */}
  {p.stock > 0 ? `Stock: ${p.stock}` : 'Agotado'}
  {/* &&: solo se muestra si la condición es verdadera */}
  {p.stock > 0 && p.stock <= 3 && <em> ¡Últimas unidades!</em>}
</li>
```

| Técnica | Condición | Cuándo se ve |
|---|---|---|
| Ternario `? :` | `p.stock > 0` | `Stock: n` si hay stock; `Agotado` si es 0 (siempre se muestra uno de los dos) |
| `&&` | `p.stock > 0 && p.stock <= 3` | `¡Últimas unidades!` solo con 1 a 3 unidades; si es falso no se muestra nada |
| `&&` | `productos.length === 0` | `No hay registros` solo con el arreglo vacío |

## Resultado 1 – arreglo con 5 registros (`captura_lista_condicional.png`)
- Ecógrafo: `Stock: 3 ¡Últimas unidades!`
- Monitor: `Stock: 8`
- Ventilador: `Stock: 2 ¡Últimas unidades!`
- Desfibrilador: `Agotado`
- Oxímetro: `Stock: 25`
- No aparece "No hay registros".

## Resultado 2 – arreglo vacío (`captura_arreglo_vacio.png`)
Se cambió temporalmente `const productos = []`: se ve `Productos (0)` y `No hay registros`, sin lista de elementos.
El arreglo original se restauró después de la prueba.

Nota: `&&` funciona porque `false && algo` da `false` y React no dibuja `false`. Con números hay que comparar (`length === 0`) y no usar `{p.stock && ...}`, porque con `0` React sí dibujaría un "0".
