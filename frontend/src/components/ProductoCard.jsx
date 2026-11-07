// Ejercicio 2 - Primer componente funcional.
// Es una función con nombre en MAYÚSCULA que devuelve JSX, y se exporta con export default.
import { productos } from '../datos.js'

function ProductoCard() {
  // Por ahora muestra siempre el primer producto; en el ejercicio 3 recibirá los datos por props.
  const p = productos[0]

  return (
    <div className="tarjeta">
      <strong>{p.nombre}</strong> — {p.marca} {p.modelo} · {p.categoria.nombre} ·
      S/ {Number(p.precio_base).toFixed(2)} · Stock: {p.stock}
    </div>
  )
}

export default ProductoCard
