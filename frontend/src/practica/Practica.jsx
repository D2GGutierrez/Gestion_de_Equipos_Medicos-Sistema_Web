// Padre de la práctica del Laboratorio 11: ES EL DUEÑO del estado del carrito (estado elevado).
// Los datos bajan por props y los avisos suben por funciones:
//   Practica -> Buscador                   (valor, onCambiar)
//   Practica -> Catalogo -> ProductoCard   (productos filtrados, onAgregar)
//   Practica -> Carrito                    (lineas, onQuitar, onVaciar)
import { useState } from 'react'
import { productos } from './datos.js'
import Catalogo from './Catalogo.jsx'
import Carrito from './Carrito.jsx'
import Buscador from './Buscador.jsx'

function Practica() {
  // Líneas del carrito: { id, nombre, precio, cantidad }
  const [carrito, setCarrito] = useState([])
  // Texto de búsqueda: también vive en el padre, porque lo comparten Buscador (lo escribe) y Catalogo (lo usa)
  const [busqueda, setBusqueda] = useState('')

  // Se filtra ANTES de entregar los productos a Catalogo (sin modificar el arreglo original)
  const texto = busqueda.trim().toLowerCase()
  const productosFiltrados = productos.filter((p) => p.nombre.toLowerCase().includes(texto))

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

  // Quitar: filter() devuelve un arreglo NUEVO sin la línea indicada (nunca splice)
  function quitarDelCarrito(id) {
    setCarrito(carrito.filter((l) => l.id !== id))
  }

  // Vaciar: se reemplaza el estado por un arreglo vacío nuevo
  function vaciarCarrito() {
    setCarrito([])
  }

  return (
    <div>
      <Buscador valor={busqueda} onCambiar={setBusqueda} />
      <Catalogo productos={productosFiltrados} onAgregar={agregarAlCarrito} />
      <Carrito lineas={carrito} onQuitar={quitarDelCarrito} onVaciar={vaciarCarrito} />
    </div>
  )
}

export default Practica
