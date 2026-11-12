// Listado: recibe el ARREGLO de equipos y las funciones por props, y dibuja una FilaEquipo por cada uno
// (map + key = id). Solo pasa las funciones hacia abajo; no cambia nada por sí mismo.
import FilaEquipo from './FilaEquipo.jsx'

function ListadoEquipos({ equipos, onEliminar, onCambiarEstado, busqueda = '' }) {
  return (
    <div>
      <h3>Equipos instalados ({equipos.length})</h3>
      {/* && : mensaje según el caso: no hay datos, o el filtro no encontró nada */}
      {equipos.length === 0 && busqueda === '' && <p className="vacio">No hay equipos registrados</p>}
      {equipos.length === 0 && busqueda !== '' && <p className="vacio">No hay equipos que coincidan con «{busqueda}»</p>}
      <ul className="lista">
        {equipos.map((e) => (
          <FilaEquipo key={e.id} equipo={e} onEliminar={onEliminar} onCambiarEstado={onCambiarEstado} />
        ))}
      </ul>
    </div>
  )
}

export default ListadoEquipos
