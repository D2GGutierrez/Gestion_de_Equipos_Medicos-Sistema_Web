// Laboratorio 12 - Ejercicios 4 a 6: GET con useEffect, estados de carga/error y alta con POST (formulario controlado).
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

  useEffect(() => {
    async function cargarClientes() {
      try {
        const respuesta = await api.get('/clientes/')
        setClientes(respuesta.data)
      } catch (err) {
        console.error('Error al pedir los clientes:', err.message)
        setError('No se pudo cargar la lista')
      } finally {
        setCargando(false)
      }
    }
    cargarClientes()
  }, [])

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

  // Muestra los mensajes de un campo (si el serializer devolvió alguno)
  function mensajes(campo) {
    return errores[campo] && errores[campo].map((m) => <span className="error" key={m}>{m}</span>)
  }

  let contenido
  if (cargando) contenido = <p className="aviso">Cargando...</p>
  else if (error) contenido = <p className="error">{error}</p>
  else if (clientes.length === 0) contenido = <p className="vacio">No hay clientes registrados</p>
  else {
    contenido = (
      <ul className="lista">
        {clientes.map((c) => (
          <li key={c.id}>
            <strong>{c.razon_social}</strong> — RUC {c.numero_identificacion} ({c.activo ? 'activo' : 'inactivo'})
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
      {contenido}
    </div>
  )
}

export default ListaPractica
