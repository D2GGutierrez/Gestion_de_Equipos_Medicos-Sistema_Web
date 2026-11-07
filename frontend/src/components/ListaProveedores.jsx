// Ejercicio 10 (investigación) - Componente lista: recibe el arreglo de proveedores por props
// y dibuja un ProveedorCard por cada uno con map() y key = id.
// Ejercicio 11 - Buscador controlado que filtra por nombre de empresa (sin distinguir mayúsculas).
// Ejercicio 12 - Formulario controlado que agrega un proveedor a la lista (estado) con validación del RUC.
import { useState } from 'react'
import ProveedorCard from './ProveedorCard.jsx'

const FORM_VACIO = { nombre_empresa: '', ruc_nit: '', contacto: '', telefono: '' }

function ListaProveedores({ proveedores: iniciales }) {
  // La lista pasa a ser ESTADO (se inicia con lo que llega por props) para poder agregar proveedores
  const [proveedores, setProveedores] = useState(iniciales)
  const [form, setForm] = useState(FORM_VACIO) // formulario controlado: un objeto con todos los campos
  const [error, setError] = useState('')
  const [busqueda, setBusqueda] = useState('') // input controlado
  const texto = busqueda.trim().toLowerCase()
  const filtrados = proveedores.filter((p) => p.nombre_empresa.toLowerCase().includes(texto))

  function manejarCambio(e) {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  function manejarSubmit(e) {
    e.preventDefault() // evita la recarga de la página al enviar el formulario

    // Validación (misma regla del serializer de la Semana 8 para el RUC): solo dígitos, 11, inicia con 10/15/17/20
    const ruc = form.ruc_nit.trim()
    if (form.nombre_empresa.trim() === '') return setError('El nombre de la empresa es obligatorio')
    if (!/^\d+$/.test(ruc)) return setError('El RUC solo debe contener dígitos')
    if (ruc.length !== 11) return setError('El RUC debe tener exactamente 11 dígitos')
    if (!['10', '15', '17', '20'].some((prefijo) => ruc.startsWith(prefijo))) {
      return setError('El RUC debe iniciar con 10, 15, 17 o 20')
    }
    if (proveedores.some((p) => p.ruc_nit === ruc)) return setError('Ya existe un proveedor con ese RUC')
    if (form.telefono.trim() === '') return setError('El teléfono es obligatorio')

    const nuevo = {
      id: Math.max(0, ...proveedores.map((p) => p.id)) + 1, // provisional: en Django lo asigna la base de datos
      nombre_empresa: form.nombre_empresa.trim(),
      ruc_nit: ruc,
      contacto: form.contacto.trim() || undefined, // vacío -> se usa el valor por defecto 'Sin contacto'
      telefono: form.telefono.trim(),
      suministros: [], // un proveedor nuevo aún no tiene suministros (relación 1:N vacía)
    }
    setProveedores([...proveedores, nuevo]) // NUEVO arreglo (spread), nunca proveedores.push(...)
    setForm(FORM_VACIO)
    setError('')
  }

  return (
    <div>
      <form className="formulario" onSubmit={manejarSubmit}>
        <input name="nombre_empresa" placeholder="Nombre de la empresa" value={form.nombre_empresa} onChange={manejarCambio} />
        <input name="ruc_nit" placeholder="RUC (11 dígitos)" value={form.ruc_nit} onChange={manejarCambio} />
        <input name="contacto" placeholder="Contacto (opcional)" value={form.contacto} onChange={manejarCambio} />
        <input name="telefono" placeholder="Teléfono" value={form.telefono} onChange={manejarCambio} />
        <button type="submit">Agregar proveedor</button>
        {error && <p className="error">{error}</p>}
      </form>

      <input
        className="buscador"
        type="text"
        placeholder="Buscar proveedor por nombre de empresa..."
        value={busqueda}
        onChange={(e) => setBusqueda(e.target.value)}
      />
      <h3>Proveedores ({filtrados.length})</h3>
      {proveedores.length === 0 && <p className="vacio">No hay registros</p>}
      {proveedores.length > 0 && filtrados.length === 0 && (
        <p className="vacio">Sin resultados para «{busqueda}»</p>
      )}
      <ul className="lista">
        {filtrados.map((p) => (
          <ProveedorCard
            key={p.id}
            nombre={p.nombre_empresa}
            ruc={p.ruc_nit}
            contacto={p.contacto}
            telefono={p.telefono}
            suministros={p.suministros}
          />
        ))}
      </ul>
    </div>
  )
}

export default ListaProveedores
