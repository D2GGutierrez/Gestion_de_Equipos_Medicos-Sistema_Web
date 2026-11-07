// Ejercicio 5 - Un equipo instalado. Los campos de la API se renombran a props más cortas:
// numero_serie -> serie, producto_nombre -> producto, precio_base -> precio.
function EquipoItem({ serie, producto, estado, precio }) {
  return (
    <li>
      {serie} — {producto} · {estado} · S/ {Number(precio).toFixed(2)}
    </li>
  )
}

export default EquipoItem
