// PADRE del panel: el estado vive AQUÍ (estado elevado) y se entrega a los hijos por props.
// Los datos bajan por props y los avisos suben por las funciones que este componente define:
//   PanelEquipos -> ResumenEquipos                 (equipos)                      [hermano del listado]
//   PanelEquipos -> BuscadorEquipos                (valor, onCambiar)
//   PanelEquipos -> FormularioEquipo               (equipos, productos, clientes, onGuardar)
//   PanelEquipos -> ListadoEquipos -> FilaEquipo   (equipos filtrados, onEliminar, onCambiarEstado)
import { useState } from 'react'
import { equiposIniciales, productosPanel, clientesPanel } from '../datosPanel.js'
import ResumenEquipos from './ResumenEquipos.jsx'
import BuscadorEquipos from './BuscadorEquipos.jsx'
import FormularioEquipo from './FormularioEquipo.jsx'
import ListadoEquipos from './ListadoEquipos.jsx'
import AvisoPanel from './AvisoPanel.jsx'

function PanelEquipos() {
  // Estado del panel: el arreglo de equipos, el texto de búsqueda y el último aviso { id, texto }
  const [equipos, setEquipos] = useState(equiposIniciales)
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState(null)

  // Búsqueda: se filtra por número de serie ANTES de entregar los equipos al listado (sin tocar el original)
  const texto = busqueda.trim().toLowerCase()
  const equiposFiltrados = equipos.filter((e) => e.numero_serie.toLowerCase().includes(texto))

  function avisar(mensaje) {
    setAviso({ id: Date.now(), texto: mensaje }) // id nuevo = el AvisoPanel se vuelve a montar
  }

  // Eliminar: filter() devuelve un arreglo NUEVO sin el equipo indicado (nunca splice)
  function eliminarEquipo(id) {
    const equipo = equipos.find((e) => e.id === id)
    setEquipos(equipos.filter((e) => e.id !== id))
    avisar(`Equipo ${equipo.numero_serie} eliminado`)
  }

  // Cambiar estado: map() devuelve un arreglo NUEVO; solo el equipo indicado se copia con otro estado
  function cambiarEstado(id) {
    const equipo = equipos.find((e) => e.id === id)
    const nuevoEstado = equipo.estado === 'OPERATIVO' ? 'MANTENIMIENTO' : 'OPERATIVO'
    setEquipos(equipos.map((e) => (e.id === id ? { ...e, estado: nuevoEstado } : e)))
    avisar(`Equipo ${equipo.numero_serie}: ahora ${nuevoEstado}`)
  }

  // Alta: el formulario entrega el registro y el padre lo agrega con un arreglo NUEVO (spread, nunca push)
  function guardarEquipo(nuevo) {
    const id = Math.max(0, ...equipos.map((e) => e.id)) + 1 // provisional: en Django lo asigna la base de datos
    setEquipos([...equipos, { id, ...nuevo }])
    avisar(`Equipo ${nuevo.numero_serie} agregado`)
  }

  return (
    <div>
      <ResumenEquipos equipos={equipos} />
      {aviso && <AvisoPanel key={aviso.id} texto={aviso.texto} />}
      <FormularioEquipo equipos={equipos} productos={productosPanel} clientes={clientesPanel} onGuardar={guardarEquipo} />
      <BuscadorEquipos valor={busqueda} onCambiar={setBusqueda} />
      <ListadoEquipos
        equipos={equiposFiltrados}
        busqueda={busqueda}
        onEliminar={eliminarEquipo}
        onCambiarEstado={cambiarEstado}
      />
    </div>
  )
}

export default PanelEquipos
