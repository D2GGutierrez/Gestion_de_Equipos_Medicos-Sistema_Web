// Laboratorio 12 - Ejercicios 4 a 8: GET con useEffect, estados de carga/error, alta con POST, DELETE, PATCH y búsqueda.
import { useEffect, useState } from 'react'
import api from '../api.js'

const vacio = { razon_social: '', numero_identificacion: '', email_contacto: '', telefono: '', direccion_fiscal: '' }

function ListaPractica() {
  const [clientes, setClientes] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)
  // Ejercicio 6: formulario controlado + errores de validación que devuelve el serializer
  const [formulario, setFormulario] = useState(vacio)
  const [errores, setErrores] = useState({})
  const [enviando, setEnviando] = useState(false)
  const [buscar, setBuscar] = useState('') // Ejercicio 8: texto del buscador (campo controlado)
  const [fallo, setFallo] = useState('') // Ejercicio 7: mensaje si falla un DELETE o un PATCH

  // Ejercicio 8: el efecto depende de [buscar]: se vuelve a ejecutar cada vez que cambia el texto
  useEffect(() => {
    let vigente = true // si el texto cambia antes de que llegue la respuesta, la respuesta vieja se ignora
    async function cargarClientes() {
      setCargando(true)
      setError(null)
      try {
        // Axios arma la URL: /clientes/?search=texto
        const respuesta = await api.get('/clientes/', { params: { search: buscar } })
        if (vigente) setClientes(respuesta.data)
      } catch (err) {
        console.error('Error al pedir los clientes:', err.message)
        if (vigente) setError('No se pudo cargar la lista')
      } finally {
        if (vigente) setCargando(false)
      }
    }
    cargarClientes()
    return () => {
      vigente = false // limpieza: se ejecuta antes de la siguiente búsqueda o al desmontar
    }
  }, [buscar])

  // Un solo manejador para todos los campos: usa el atributo name del input
  function cambiar(e) {
    setFormulario({ ...formulario, [e.target.name]: e.target.value })
  }

  async function enviar(e) {
    e.preventDefault() // evita que el navegador recargue la página
    setEnviando(true)
    setErrores({})
    try {
      const respuesta = await api.post('/clientes/', formulario) // POST -> 201 con el registro creado
      setClientes([...clientes, respuesta.data]) // arreglo NUEVO con el registro que devolvió el servidor
      setFormulario(vacio)
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setErrores(err.response.data) // 400: { campo: ["mensaje", ...] } enviado por validate_<campo>
      } else {
        setErrores({ general: ['No se pudo guardar el cliente'] })
      }
    } finally {
      setEnviando(false)
    }
  }

  // Ejercicio 7 - DELETE: se quita del estado SOLO cuando el servidor confirma con 204
  async function eliminar(id) {
    setFallo('')
    try {
      await api.delete(`/clientes/${id}/`) // 204 No Content (sin cuerpo)
      setClientes(clientes.filter((c) => c.id !== id)) // arreglo NUEVO sin el cliente eliminado
    } catch {
      setFallo('No se pudo eliminar el cliente')
    }
  }

  // Ejercicio 7 - PATCH: envía solo el campo que cambia; el estado se actualiza con map()
  async function cambiarActivo(cliente) {
    setFallo('')
    try {
      const respuesta = await api.patch(`/clientes/${cliente.id}/`, { activo: !cliente.activo }) // 200 con el registro completo
      setClientes(clientes.map((c) => (c.id === cliente.id ? respuesta.data : c)))
    } catch {
      setFallo('No se pudo modificar el cliente')
    }
  }

  // Muestra los mensajes de un campo (si el serializer devolvió alguno)
  function mensajes(campo) {
    return errores[campo] && errores[campo].map((m) => <span className="error" key={m}>{m}</span>)
  }

  let contenido
  if (cargando) contenido = <p className="aviso">Cargando...</p>
  else if (error) contenido = <p className="error">{error}</p>
  else if (clientes.length === 0 && buscar === '') contenido = <p className="vacio">No hay clientes registrados</p>
  else if (clientes.length === 0) contenido = <p className="vacio">No hay clientes que coincidan con «{buscar}»</p>
  else {
    contenido = (
      <ul className="lista lista-api">
        {clientes.map((c) => (
          <li key={c.id}>
            <strong>{c.razon_social}</strong> — RUC {c.numero_identificacion} ({c.activo ? 'activo' : 'inactivo'})
            <button className="boton-accion" onClick={() => cambiarActivo(c)}>{c.activo ? 'Desactivar' : 'Activar'}</button>
            <button className="boton-quitar" onClick={() => eliminar(c.id)}>Eliminar</button>
          </li>
        ))}
      </ul>
    )
  }

  return (
    <div>
      <form className="formulario" onSubmit={enviar}>
        <input name="razon_social" placeholder="Razón social" value={formulario.razon_social} onChange={cambiar} required />
        {mensajes('razon_social')}
        <input name="numero_identificacion" placeholder="RUC (11 dígitos)" value={formulario.numero_identificacion} onChange={cambiar} required />
        {mensajes('numero_identificacion')}
        <input name="email_contacto" type="email" placeholder="Correo de contacto" value={formulario.email_contacto} onChange={cambiar} required />
        {mensajes('email_contacto')}
        <input name="telefono" placeholder="Teléfono" value={formulario.telefono} onChange={cambiar} required />
        {mensajes('telefono')}
        <input name="direccion_fiscal" placeholder="Dirección fiscal" value={formulario.direccion_fiscal} onChange={cambiar} required />
        {mensajes('direccion_fiscal')}
        {mensajes('general')}
        <button type="submit" disabled={enviando}>{enviando ? 'Guardando...' : 'Agregar cliente'}</button>
      </form>
      <input
        className="buscador"
        placeholder="Buscar por razón social o RUC..."
        value={buscar}
        onChange={(e) => setBuscar(e.target.value)}
      />
      {fallo && <p className="error">{fallo}</p>}
      {contenido}
    </div>
  )
}

export default ListaPractica
