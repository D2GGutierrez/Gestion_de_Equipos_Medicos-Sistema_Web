// Listado: recibe el ARREGLO de equipos y las funciones por props, y dibuja una FilaEquipo por cada uno
// (map + key = id). Solo pasa las funciones hacia abajo; no cambia nada por sí mismo.
import FilaEquipo from './FilaEquipo.jsx'

function ListadoEquipos({ equipos, onEliminar, onCambiarEstado }) {
  return (
    <div>
      <h3>Equipos instalados ({equipos.length})</h3>
      {equipos.length === 0 && <p className="vacio">No hay equipos registrados</p>}
      <ul className="lista">
        {equipos.map((e) => (
          <FilaEquipo key={e.id} equipo={e} onEliminar={onEliminar} onCambiarEstado={onCambiarEstado} />
        ))}
      </ul>
    </div>
  )
}

export default ListadoEquipos
