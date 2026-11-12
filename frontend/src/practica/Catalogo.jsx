// Hijo de Practica: recibe el arreglo de productos y la función onAgregar, y las pasa hacia abajo.
import ProductoCard from './ProductoCard.jsx'

function Catalogo({ productos, onAgregar }) {
  return (
    <div>
      <h3>Catálogo</h3>
      <ul className="lista">
        {productos.map((p) => (
          <ProductoCard key={p.id} producto={p} onAgregar={onAgregar} />
        ))}
      </ul>
    </div>
  )
}

export default Catalogo
