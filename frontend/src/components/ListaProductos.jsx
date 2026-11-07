// Ejercicio 3 - Segundo componente: recibe el ARREGLO de productos por props y
// dibuja un ProductoCard por cada uno con map(), con key basada en el id.
// Ejercicio 7 - Buscador controlado: el texto vive en un estado y la lista se filtra al escribir.
// Ejercicio 8 - Formulario controlado: agrega productos a la lista (estado) con validación.
import { useState } from 'react'
import ProductoCard from './ProductoCard.jsx'

const FORM_VACIO = { nombre: '', marca: '', modelo: '', precio: '', stock: '' }

function ListaProductos({ productos: iniciales }) {
  // La lista pasa a ser ESTADO (se inicia con lo que llega por props) para poder agregar productos
  const [productos, setProductos] = useState(iniciales)
  // Formulario controlado: un solo objeto de estado con todos los campos
  const [form, setForm] = useState(FORM_VACIO)
  const [error, setError] = useState('')
  // Input CONTROLADO: React es la "fuente de verdad" del texto (value + onChange)
  const [busqueda, setBusqueda] = useState('')

  // No se modifica el arreglo original: se calcula uno nuevo en cada renderizado.
  // toLowerCase() en ambos lados para que no distinga mayúsculas de minúsculas.
  const texto = busqueda.trim().toLowerCase()
  const filtrados = productos.filter((p) => p.nombre.toLowerCase().includes(texto))

  // Un solo manejador para todos los campos: usa el atributo name del input
  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarSubmit(e) {
    e.preventDefault() // evita que el navegador recargue la página al enviar el form

    // Validación (reglas de la API de la Semana 8): nombre obligatorio, precio > 0, stock entero >= 0
    if (form.nombre.trim() === '') return setError('El nombre es obligatorio')
    if (!(Number(form.precio) > 0)) return setError('El precio debe ser mayor a 0')
    if (!Number.isInteger(Number(form.stock)) || Number(form.stock) < 0 || form.stock === '') {
      return setError('El stock debe ser un número entero mayor o igual a 0')
    }

    const nuevo = {
      id: Math.max(0, ...productos.map((p) => p.id)) + 1, // provisional: en Django lo asigna la base de datos
      nombre: form.nombre.trim(),
      marca: form.marca.trim() || undefined, // sin marca -> se usa el valor por defecto de ProductoCard
      modelo: form.modelo.trim(),
      precio_base: form.precio,
      stock: Number(form.stock),
      categoria: { id: 0, nombre: 'Sin categoría' },
    }
    setProductos([...productos, nuevo]) // NUEVO arreglo (spread), nunca productos.push(...)
    setForm(FORM_VACIO) // limpia los campos
    setError('')
  }

  return (
    <div>
      <form className="formulario" onSubmit={manejarSubmit}>
        <input name="nombre" placeholder="Nombre" value={form.nombre} onChange={manejarCambio} />
        <input name="marca" placeholder="Marca (opcional)" value={form.marca} onChange={manejarCambio} />
        <input name="modelo" placeholder="Modelo" value={form.modelo} onChange={manejarCambio} />
        <input name="precio" type="number" step="0.01" placeholder="Precio" value={form.precio} onChange={manejarCambio} />
        <input name="stock" type="number" placeholder="Stock" value={form.stock} onChange={manejarCambio} />
        <button type="submit">Agregar producto</button>
        {error && <p className="error">{error}</p>}
      </form>

      <input
        className="buscador"
        type="text"
        placeholder="Buscar producto por nombre..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />

      <h3>Productos ({filtrados.length})</h3>

      {/* && : mensajes según el caso: no hay datos, o la búsqueda no encontró nada */}
      {productos.length === 0 && <p className="vacio">No hay registros</p>}
      {productos.length > 0 && filtrados.length === 0 && (
        <p className="vacio">Sin resultados para «{busqueda}»</p>
      )}

      <ul className="lista">
        {filtrados.map((p) => (
          <ProductoCard
            key={p.id}
            nombre={p.nombre}
            marca={p.marca}
            modelo={p.modelo}
            categoria={p.categoria.nombre}
            precio={p.precio_base}   // el dato de la API se llama precio_base; la prop se llama precio
            stock={p.stock}
          />
        ))}
      </ul>
    </div>
  )
}

export default ListaProductos
