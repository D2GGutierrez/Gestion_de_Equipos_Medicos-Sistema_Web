# Ejercicio 11 – Renderizado condicional y estilos

Archivos: `frontend/src/App.jsx` y `frontend/src/App.css` (archivo CSS propio, importado con `import './App.css'`).

## Renderizado condicional
```jsx
{/* ternario: una cosa u otra */}
{p.stock > 0 ? `Stock: ${p.stock}` : <span className="agotado">Agotado</span>}

{/* &&: solo si la condición es verdadera */}
{p.stock > 0 && p.stock <= 3 && <em className="ultimas"> ¡Últimas unidades!</em>}

{/* lista vacía, una por cada lista */}
{productos.length === 0 && <p className="vacio">No hay registros</p>}
{clientes.length === 0 && <p className="vacio">No hay clientes registrados</p>}
```

## Estilos
- **`className` + `App.css`** (8 reglas): `.app`, `.titulo`, `.tarjeta`, `.agotado` (rojo), `.ultimas` (naranja), `.vacio` (gris cursiva), `.lista`, `.equipos`.
- **`style={{ }}`** (estilo en línea): `<p style={{ fontWeight: 'bold', color: '#065f46' }}>Total de equipos: S/ …</p>`.

## Resultados
- `captura_con_datos.png`: con datos se ve `Agotado` en rojo, `¡Últimas unidades!` en naranja (stock 1 a 3), el stock normal en el resto, y los totales en verde.
- `captura_listas_vacias.png`: con ambos arreglos vaciados temporalmente se ve `Productos (0)` + `No hay registros` y, en la segunda lista, `No hay clientes registrados`. Los arreglos se restauraron después.
- `npm run lint`: sin avisos (código de salida 0). `npm run build`: correcto. Sin advertencias en la consola.
