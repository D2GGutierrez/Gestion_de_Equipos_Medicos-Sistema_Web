// Ejercicio 10 (investigación) - Componente lista: recibe el arreglo de proveedores por props
// y dibuja un ProveedorCard por cada uno con map() y key = id.
import ProveedorCard from './ProveedorCard.jsx'

function ListaProveedores({ proveedores }) {
  return (
    <div>
      <h3>Proveedores ({proveedores.length})</h3>
      {proveedores.length === 0 && <p className="vacio">No hay registros</p>}
      <ul className="lista">
        {proveedores.map((p) => (
          <ProveedorCard
            key={p.id}
            nombre={p.nombre_empresa}
            ruc={p.ruc_nit}
            contacto={p.contacto}
            telefono={p.telefono}
            suministros={p.suministros}
          />
        ))}
      </ul>
    </div>
  )
}

export default ListaProveedores
