// Padre de la práctica del Laboratorio 11: ES EL DUEÑO del estado del carrito (estado elevado).
// Los datos bajan por props y los avisos suben por funciones:
//   Practica -> Catalogo -> ProductoCard   (productos, onAgregar)
//   Practica -> Carrito                    (lineas)
import { useState } from 'react'
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'
import Carrito from './Carrito.jsx'

function Practica() {
  // Líneas del carrito: { id, nombre, precio, cantidad }
  const [carrito, setCarrito] = useState([])

  function agregarAlCarrito(producto) {
    const existe = carrito.some((l) => l.id === producto.id)
    if (existe) {
      // Ya está: map() devuelve un arreglo NUEVO con la cantidad aumentada en esa línea
      setCarrito(carrito.map((l) => (l.id === producto.id ? { ...l, cantidad: l.cantidad + 1 } : l)))
    } else {
      // No está: arreglo nuevo con spread (nunca carrito.push)
      setCarrito([...carrito, { id: producto.id, nombre: producto.nombre, precio: producto.precio, cantidad: 1 }])
    }
  }

  return (
    <div>
      <Catalogo productos={productos} onAgregar={agregarAlCarrito} />
      <Carrito lineas={carrito} />
    </div>
  )
}

export default Practica
