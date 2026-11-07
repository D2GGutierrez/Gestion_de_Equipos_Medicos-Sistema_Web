// Ejercicio 3 - El componente recibe los datos del registro por props (desestructuradas).
// "marca" tiene un valor por defecto: si no se envía esa prop, se usa 'Sin marca'.
// Ejercicio 6 - Cada tarjeta guarda su propio contador con useState (estado independiente).
import { useState } from 'react'

function ProductoCard({ nombre, marca = 'Sin marca', modelo, categoria, precio, stock }) {
  // cantidad = valor actual; setCantidad = única forma de cambiarlo (React vuelve a dibujar)
  const [cantidad, setCantidad] = useState(0)

  return (
    <li className="tarjeta">
      <strong>{nombre}</strong> — {marca} {modelo} · {categoria} ·
      S/ {Number(precio).toFixed(2)} ·{' '}
      {stock > 0 ? `Stock: ${stock}` : <span className="agotado">Agotado</span>}
      {stock > 0 && stock <= 3 && <em className="ultimas"> ¡Últimas unidades!</em>}
      <div className="acciones">
        {/* disabled según un campo del registro: sin stock, o ya se pidió todo el stock */}
        <button onClick={() => setCantidad(cantidad + 1)} disabled={stock === 0 || cantidad >= stock}>
          Agregar al pedido
        </button>
        {/* && : solo se muestra si hay al menos 1 unidad en el pedido */}
        {cantidad > 0 && <span className="pedido">En pedido: {cantidad}</span>}
      </div>
    </li>
  )
}

export default ProductoCard
