// PADRE del panel: el estado de los equipos vive AQUÍ (estado elevado) y se entrega a los hijos por props.
//   PanelEquipos -> ListadoEquipos (equipos) -> FilaEquipo (equipo)
import { useState } from 'react'
import { equiposIniciales } from '../datosPanel.js'
import ListadoEquipos from './ListadoEquipos.jsx'

function PanelEquipos() {
  // Único lugar donde se guarda el arreglo de equipos (forma de la respuesta de la API)
  // (la función para cambiarlo, setEquipos, se agrega en los ejercicios 11 y 12)
  const [equipos] = useState(equiposIniciales)

  return <ListadoEquipos equipos={equipos} />
}

export default PanelEquipos
