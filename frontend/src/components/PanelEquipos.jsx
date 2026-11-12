// PADRE del panel: el estado de los equipos vive AQUÍ (estado elevado) y se entrega a los hijos por props.
// Los datos bajan por props y los avisos suben por las funciones que este componente define:
//   PanelEquipos -> ListadoEquipos -> FilaEquipo   (equipos / equipo, onEliminar, onCambiarEstado)
//   PanelEquipos -> FormularioEquipo               (equipos, productos, clientes, onGuardar)
import { useState } from 'react'
import { equiposIniciales, productosPanel, clientesPanel } from '../datosPanel.js'
import ListadoEquipos from './ListadoEquipos.jsx'
import FormularioEquipo from './FormularioEquipo.jsx'

function PanelEquipos() {
  // Único lugar donde se guarda el arreglo de equipos (forma de la respuesta de la API)
  const [equipos, setEquipos] = useState(equiposIniciales)

  // Eliminar: filter() devuelve un arreglo NUEVO sin el equipo indicado (nunca splice)
  function eliminarEquipo(id) {
    setEquipos(equipos.filter((e) => e.id !== id))
  }

  // Cambiar estado: map() devuelve un arreglo NUEVO; solo el equipo indicado se copia con otro estado
  function cambiarEstado(id) {
    setEquipos(
      equipos.map((e) =>
        e.id === id ? { ...e, estado: e.estado === 'OPERATIVO' ? 'MANTENIMIENTO' : 'OPERATIVO' } : e,
      ),
    )
  }

  // Alta: el formulario entrega el registro y el padre lo agrega con un arreglo NUEVO (spread, nunca push)
  function guardarEquipo(nuevo) {
    const id = Math.max(0, ...equipos.map((e) => e.id)) + 1 // provisional: en Django lo asigna la base de datos
    setEquipos([...equipos, { id, ...nuevo }])
  }

  return (
    <div>
      <FormularioEquipo equipos={equipos} productos={productosPanel} clientes={clientesPanel} onGuardar={guardarEquipo} />
      <ListadoEquipos equipos={equipos} onEliminar={eliminarEquipo} onCambiarEstado={cambiarEstado} />
    </div>
  )
}

export default PanelEquipos
