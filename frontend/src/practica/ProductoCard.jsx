// Hijo (nieto de Practica): recibe UN producto y la función onAgregar por props.
// Cuando el usuario hace clic, AVISA al padre llamando a onAgregar(producto).
function ProductoCard({ producto, onAgregar }) {
  return (
    <li className="tarjeta">
      <strong>{producto.nombre}</strong> · S/ {Number(producto.precio).toFixed(2)}
      {producto.stock === 0 && <span className="agotado"> Agotado</span>}
      <div className="acciones">
        {/* () => onAgregar(producto): se ejecuta SOLO al hacer clic. Desactivado si no hay stock */}
        <button onClick={() => onAgregar(producto)} disabled={producto.stock === 0}>
          Agregar
        </button>
      </div>
    </li>
  )
}

export default ProductoCard
