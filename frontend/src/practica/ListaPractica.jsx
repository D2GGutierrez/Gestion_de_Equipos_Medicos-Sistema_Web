// Laboratorio 12 - Ejercicio 4: GET a la API de Django con Axios dentro de useEffect.
import { useEffect, useState } from 'react'
import api from '../api.js'

function ListaPractica() {
  // Estado: la lista que llega del servidor (empieza vacía)
  const [clientes, setClientes] = useState([])

  // [] = la petición se hace UNA vez, cuando el componente aparece en pantalla.
  // La función del efecto NO es async (React espera una función de limpieza o nada, no una promesa):
  // se declara una función async adentro y se llama.
  useEffect(() => {
    async function cargarClientes() {
      const respuesta = await api.get('/clientes/') // GET http://127.0.0.1:8000/api/clientes/
      setClientes(respuesta.data) // el JSON ya llega convertido en un arreglo
    }
    cargarClientes()
  }, [])

  return (
    <ul className="lista">
      {/* key basada en el id que entrega la base de datos */}
      {clientes.map((c) => (
        <li key={c.id}>
          <strong>{c.razon_social}</strong> — RUC {c.numero_identificacion} ({c.activo ? 'activo' : 'inactivo'})
        </li>
      ))}
    </ul>
  )
}

export default ListaPractica
