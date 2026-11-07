// Ejercicio 5 - Un cliente con sus equipos (relación 1:N). Recibe por props:
// razonSocial (razon_social de la API) y equipos (arreglo). Las props NO se modifican:
// el total se CALCULA a partir de ellas, no se guarda cambiando los datos recibidos.
import EquipoItem from './EquipoItem.jsx'

function ClienteCard({ razonSocial, equipos }) {
  const total = equipos.reduce((suma, e) => suma + Number(e.precio_base), 0)

  return (
    <li className="tarjeta">
      <strong>{razonSocial}</strong> ({equipos.length} {equipos.length === 1 ? 'equipo' : 'equipos'})
      {equipos.length === 0 && <p className="vacio">Sin equipos instalados</p>}
      <ul className="equipos">
        {equipos.map((e) => (
          <EquipoItem key={e.id} serie={e.numero_serie} producto={e.producto_nombre} estado={e.estado} precio={e.precio_base} />
        ))}
      </ul>
      <p style={{ fontWeight: 'bold', color: '#065f46' }}>Total de equipos: S/ {total.toFixed(2)}</p>
    </li>
  )
}

export default ClienteCard
