// Padre de la práctica del Laboratorio 11: tiene los datos y las funciones.
// Los datos bajan por props (productos -> producto) y los avisos suben por funciones (onAgregar).
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'

function Practica() {
  // Por ahora solo muestra en consola; en el Ejercicio 4 actualizará el carrito
  function agregarAlCarrito(producto) {
    console.log('Agregar al carrito:', producto.nombre)
  }

  return <Catalogo productos={productos} onAgregar={agregarAlCarrito} />
}

export default Practica
