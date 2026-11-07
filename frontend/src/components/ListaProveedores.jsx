// Ejercicio 10 (investigación) - Componente lista: recibe el arreglo de proveedores por props
// y dibuja un ProveedorCard por cada uno con map() y key = id.
// Ejercicio 11 - Buscador controlado que filtra por nombre de empresa (sin distinguir mayúsculas).
import { useState } from 'react'
import ProveedorCard from './ProveedorCard.jsx'

function ListaProveedores({ proveedores }) {
  const [busqueda, setBusqueda] = useState('') // input controlado
  const texto = busqueda.trim().toLowerCase()
  const filtrados = proveedores.filter((p) => p.nombre_empresa.toLowerCase().includes(texto))

  return (
    <div>
      <input
        className="buscador"
        type="text"
        placeholder="Buscar proveedor por nombre de empresa..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />
      <h3>Proveedores ({filtrados.length})</h3>
      {proveedores.length === 0 && <p className="vacio">No hay registros</p>}
      {proveedores.length > 0 && filtrados.length === 0 && (
        <p className="vacio">Sin resultados para «{busqueda}»</p>
      )}
      <ul className="lista">
        {filtrados.map((p) => (
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
