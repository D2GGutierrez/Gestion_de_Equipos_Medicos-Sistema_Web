// Hijo de Practica: recibe el ARREGLO de productos por props y entrega cada producto a ProductoCard.
import ProductoCard from './ProductoCard.jsx'

function Catalogo({ productos }) {
  return (
    <div>
      <h3>Catálogo</h3>
      <ul className="lista">
        {productos.map((p) => (
          <ProductoCard key={p.id} producto={p} />
        ))}
      </ul>
    </div>
  )
}

export default Catalogo
