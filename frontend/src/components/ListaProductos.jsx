// Ejercicio 3 - Segundo componente: recibe el ARREGLO de productos por props y
// dibuja un ProductoCard por cada uno con map(), con key basada en el id.
// Ejercicio 7 - Buscador controlado: el texto vive en un estado y la lista se filtra al escribir.
import { useState } from 'react'
import ProductoCard from './ProductoCard.jsx'

function ListaProductos({ productos }) {
  // Input CONTROLADO: React es la "fuente de verdad" del texto (value + onChange)
  const [busqueda, setBusqueda] = useState('')

  // No se modifica el arreglo original: se calcula uno nuevo en cada renderizado.
  // toLowerCase() en ambos lados para que no distinga mayúsculas de minúsculas.
  const texto = busqueda.trim().toLowerCase()
  const filtrados = productos.filter((p) => p.nombre.toLowerCase().includes(texto))

  return (
    <div>
      <input
        className="buscador"
        type="text"
        placeholder="Buscar producto por nombre..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />

      <h3>Productos ({filtrados.length})</h3>

      {/* && : mensajes según el caso: no hay datos, o la búsqueda no encontró nada */}
      {productos.length === 0 && <p className="vacio">No hay registros</p>}
      {productos.length > 0 && filtrados.length === 0 && (
        <p className="vacio">Sin resultados para «{busqueda}»</p>
      )}

      <ul className="lista">
        {filtrados.map((p) => (
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
