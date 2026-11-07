// Ejercicio 3 - Segundo componente: recibe el ARREGLO de productos por props y
// dibuja un ProductoCard por cada uno con map(), con key basada en el id.
import ProductoCard from './ProductoCard.jsx'

function ListaProductos({ productos }) {
  return (
    <div>
      <h3>Productos ({productos.length})</h3>

      {/* && : el mensaje solo aparece si el arreglo está vacío */}
      {productos.length === 0 && <p className="vacio">No hay registros</p>}

      <ul className="lista">
        {productos.map((p) => (
          <ProductoCard
            key={p.id}
            nombre={p.nombre}
            marca={p.marca}
            modelo={p.modelo}
            categoria={p.categoria.nombre}
            precio={p.precio_base}   // el dato de la API se llama precio_base; la prop se llama precio
            stock={p.stock}
          />
        ))}
      </ul>
    </div>
  )
}

export default ListaProductos
