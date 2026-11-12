// Formulario de alta (hijo): campos CONTROLADOS (value + onChange). Valida antes de enviar y, si todo
// está bien, entrega el equipo nuevo al padre con onGuardar(equipo). No agrega nada a la lista por sí mismo.
import { useState } from 'react'

const FORM_VACIO = { numero_serie: '', producto: '', cliente: '', fecha_instalacion: '', estado: 'OPERATIVO' }

// fin_garantia = fecha de instalación + meses de garantía del producto (formato AAAA-MM-DD)
function sumarMeses(fecha, meses) {
  const [anio, mes, dia] = fecha.split('-').map(Number)
  const d = new Date(anio, mes - 1 + meses, dia)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

function FormularioEquipo({ equipos, productos, clientes, onGuardar }) {
  const [form, setForm] = useState(FORM_VACIO)
  const [error, setError] = useState('')

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarSubmit(e) {
    e.preventDefault()

    // Reglas del modelo EquipoInstalado / API de la Semana 8
    const serie = form.numero_serie.trim().toUpperCase()
    if (serie === '') return setError('El número de serie es obligatorio')
    if (equipos.some((eq) => eq.numero_serie.toUpperCase() === serie)) {
      return setError('Ya existe un equipo con ese número de serie')
    }
    if (form.producto === '') return setError('Seleccione un producto')
    if (form.cliente === '') return setError('Seleccione un cliente')
    if (form.fecha_instalacion === '') return setError('La fecha de instalación es obligatoria')
    if (form.fecha_instalacion > new Date().toISOString().slice(0, 10)) {
      return setError('La fecha de instalación no puede ser futura')
    }

    const producto = productos.find((p) => p.id === Number(form.producto))
    const cliente = clientes.find((c) => c.id === Number(form.cliente))
    // Registro con la forma de la API (sin id: lo asigna el padre / la base de datos)
    onGuardar({
      numero_serie: serie,
      fecha_instalacion: form.fecha_instalacion,
      fin_garantia: sumarMeses(form.fecha_instalacion, producto.meses_garantia),
      estado: form.estado,
      producto: producto.id,
      producto_nombre: producto.nombre,
      cliente: cliente.id,
      cliente_razon_social: cliente.razon_social,
    })
    setForm(FORM_VACIO) // campos vacíos tras un alta correcta
    setError('')
  }

  return (
    <form className="formulario" onSubmit={manejarSubmit}>
      <input name="numero_serie" placeholder="Número de serie" value={form.numero_serie} onChange={manejarCambio} />
      <select name="producto" value={form.producto} onChange={manejarCambio}>
        <option value="">Producto...</option>
        {productos.map((p) => (
          <option key={p.id} value={p.id}>{p.nombre}</option>
        ))}
      </select>
      <select name="cliente" value={form.cliente} onChange={manejarCambio}>
        <option value="">Cliente...</option>
        {clientes.map((c) => (
          <option key={c.id} value={c.id}>{c.razon_social}</option>
        ))}
      </select>
      <input name="fecha_instalacion" type="date" value={form.fecha_instalacion} onChange={manejarCambio} />
      <select name="estado" value={form.estado} onChange={manejarCambio}>
        <option value="OPERATIVO">Operativo</option>
        <option value="MANTENIMIENTO">En mantenimiento</option>
        <option value="INACTIVO">Inactivo</option>
      </select>
      <button type="submit">Agregar equipo</button>
      {error && <p className="error">{error}</p>}
    </form>
  )
}

export default FormularioEquipo
