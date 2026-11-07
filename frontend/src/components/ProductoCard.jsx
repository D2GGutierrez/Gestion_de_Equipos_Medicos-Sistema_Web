// Ejercicio 3 - El componente recibe los datos del registro por props (desestructuradas).
// "marca" tiene un valor por defecto: si no se envía esa prop, se usa 'Sin marca'.
function ProductoCard({ nombre, marca = 'Sin marca', modelo, categoria, precio, stock }) {
  return (
    <li className="tarjeta">
      <strong>{nombre}</strong> — {marca} {modelo} · {categoria} ·
      S/ {Number(precio).toFixed(2)} ·{' '}
      {/* ternario: una cosa u otra según el stock */}
      {stock > 0 ? `Stock: ${stock}` : <span className="agotado">Agotado</span>}
      {/* &&: solo se muestra si la condición es verdadera */}
      {stock > 0 && stock <= 3 && <em className="ultimas"> ¡Últimas unidades!</em>}
    </li>
  )
}

export default ProductoCard
