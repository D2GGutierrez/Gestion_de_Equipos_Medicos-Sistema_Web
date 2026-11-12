// Padre de la práctica del Laboratorio 11: tiene los datos y los entrega hacia abajo por props.
// Flujo: Practica -> Catalogo (productos) -> ProductoCard (producto)
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'

function Practica() {
  return <Catalogo productos={productos} />
}

export default Practica
