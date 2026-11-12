// Hijo (nieto de Practica): recibe UN producto por props y lo muestra.
function ProductoCard({ producto }) {
  return (
    <li className="tarjeta">
      <strong>{producto.nombre}</strong> · S/ {Number(producto.precio).toFixed(2)}
      {producto.stock === 0 && <span className="agotado"> Agotado</span>}
    </li>
  )
}

export default ProductoCard
