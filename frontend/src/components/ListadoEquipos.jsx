// Listado: recibe el ARREGLO de equipos por props y dibuja una FilaEquipo por cada uno (map + key = id).
import FilaEquipo from './FilaEquipo.jsx'

function ListadoEquipos({ equipos }) {
  return (
    <div>
      <h3>Equipos instalados ({equipos.length})</h3>
      {equipos.length === 0 && <p className="vacio">No hay equipos registrados</p>}
      <ul className="lista">
        {equipos.map((e) => (
          <FilaEquipo key={e.id} equipo={e} />
        ))}
      </ul>
    </div>
  )
}

export default ListadoEquipos
