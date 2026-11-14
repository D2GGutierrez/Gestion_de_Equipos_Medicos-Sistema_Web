// Laboratorio 12 - Ejercicios 4 y 5: GET a la API con Axios dentro de useEffect, con estados de carga y de error.
import { useEffect, useState } from 'react'
import api from '../api.js'

function ListaPractica() {
  const [clientes, setClientes] = useState([])
  const [cargando, setCargando] = useState(true) // true desde el inicio: lo primero que se ve es "Cargando..."
  const [error, setError] = useState(null)

  useEffect(() => {
    async function cargarClientes() {
      try {
        const respuesta = await api.get('/clientes/')
        setClientes(respuesta.data)
      } catch (err) {
        console.error('Error al pedir los clientes:', err.message) // detalle técnico solo en la consola
        setError('No se pudo cargar la lista') // mensaje claro para el usuario
      } finally {
        setCargando(false) // se ejecuta SIEMPRE: con éxito o con error, la carga terminó
      }
    }
    cargarClientes()
  }, [])

  // Los tres estados de la pantalla (más la lista con datos)
  if (cargando) return <p className="aviso">Cargando...</p>
  if (error) return <p className="error">{error}</p>
  if (clientes.length === 0) return <p className="vacio">No hay clientes registrados</p>

  return (
    <ul className="lista">
      {clientes.map((c) => (
        <li key={c.id}>
          <strong>{c.razon_social}</strong> — RUC {c.numero_identificacion} ({c.activo ? 'activo' : 'inactivo'})
        </li>
      ))}
    </ul>
  )
}

export default ListaPractica
