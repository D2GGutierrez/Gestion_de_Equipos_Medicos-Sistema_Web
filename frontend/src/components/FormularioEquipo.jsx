// Formulario de alta y edición (hijo): campos CONTROLADOS (value + onChange).
// Lab 12 Ej 11: ya no agrega nada por sí mismo ni valida la serie: arma el registro y lo entrega al padre con
// onGuardar(datos). El padre decide si es POST (alta) o PATCH (edición) y devuelve los errores 400 de la API en "errores".
import { useState } from 'react'

const ETIQUETAS = {
  numero_serie: 'Número de serie',
  producto: 'Producto',
  cliente: 'Cliente',
  fecha_instalacion: 'Fecha de instalación',
  fin_garantia: 'Fin de garantía',
  estado: 'Estado',
}

// fin_garantia = fecha de instalación + meses de garantía del producto (formato AAAA-MM-DD)
function sumarMeses(fecha, meses) {
  const [anio, mes, dia] = fecha.split('-').map(Number)
  const d = new Date(anio, mes - 1 + meses, dia)
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
}

// Convierte { campo: ["mensaje", ...] } (formato de DRF) en una lista de textos legibles
function textosDeErrores(errores) {
  return Object.entries(errores).flatMap(([campo, mensajes]) => {
    const lista = Array.isArray(mensajes) ? mensajes : [String(mensajes)]
    const etiqueta = ETIQUETAS[campo]
    return lista.map((m) => (etiqueta ? `${etiqueta}: ${m}` : m))
  })
}

function FormularioEquipo({ productos, clientes, equipoEditando, errores, guardando, onGuardar, onCancelar }) {
  // Estado inicial: vacío para un alta, o con los datos del equipo seleccionado para editar.
  // El padre cambia la "key" del formulario cuando cambia el equipo seleccionado, así el estado se reinicia.
  const [form, setForm] = useState(
    equipoEditando
      ? {
          numero_serie: equipoEditando.numero_serie,
          producto: String(equipoEditando.producto),
          cliente: String(equipoEditando.cliente),
          fecha_instalacion: equipoEditando.fecha_instalacion,
          estado: equipoEditando.estado,
        }
      : { numero_serie: '', producto: '', cliente: '', fecha_instalacion: '', estado: 'OPERATIVO' },
  )
  const [errorLocal, setErrorLocal] = useState('')

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarSubmit(e) {
    e.preventDefault()
    // Solo campos vacíos; el formato y la unicidad del número de serie los valida la API (validate_numero_serie)
    if (form.numero_serie.trim() === '') return setErrorLocal('El número de serie es obligatorio')
    if (form.producto === '') return setErrorLocal('Seleccione un producto')
    if (form.cliente === '') return setErrorLocal('Seleccione un cliente')
    if (form.fecha_instalacion === '') return setErrorLocal('La fecha de instalación es obligatoria')
    setErrorLocal('')

    const producto = productos.find((p) => p.id === Number(form.producto))
    // En edición, si no cambió ni la fecha ni el producto, se conserva la garantía que ya tenía el equipo
    const conservarGarantia =
      equipoEditando &&
      equipoEditando.fecha_instalacion === form.fecha_instalacion &&
      equipoEditando.producto === producto.id
    onGuardar({
      numero_serie: form.numero_serie.trim(),
      fecha_instalacion: form.fecha_instalacion,
      fin_garantia: conservarGarantia ? equipoEditando.fin_garantia : sumarMeses(form.fecha_instalacion, producto.meses_garantia),
      estado: form.estado,
      producto: producto.id,
      cliente: Number(form.cliente),
    })
  }

  return (
    <form className="formulario" onSubmit={manejarSubmit}>
      <input name="numero_serie" placeholder="Número de serie (ej. ECO-0003)" value={form.numero_serie} onChange={manejarCambio} />
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
      <button type="submit" disabled={guardando}>
        {guardando ? 'Guardando...' : equipoEditando ? 'Guardar cambios' : 'Agregar equipo'}
      </button>
      {equipoEditando && (
        <button type="button" className="boton-cancelar" onClick={onCancelar}>Cancelar edición</button>
      )}
      {errorLocal && <p className="error">{errorLocal}</p>}
      {/* Mensajes 400 que envía el serializer de Django, junto al formulario */}
      {textosDeErrores(errores).map((t) => (
        <p className="error" key={t}>{t}</p>
      ))}
    </form>
  )
}

export default FormularioEquipo
