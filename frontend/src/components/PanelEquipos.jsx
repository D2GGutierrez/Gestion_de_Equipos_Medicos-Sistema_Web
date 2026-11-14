// Lab 12 Ej 10 y 11: los datos vienen de la API de Django (GET con useEffect) y el alta y la edición se envían con POST y PATCH.
// PADRE del panel: el estado vive AQUÍ (estado elevado) y se entrega a los hijos por props.
// Los datos bajan por props y los avisos suben por las funciones que este componente define:
//   PanelEquipos -> ResumenEquipos                 (equipos)                      [hermano del listado]
//   PanelEquipos -> BuscadorEquipos                (valor, onCambiar)
//   PanelEquipos -> FormularioEquipo               (productos, clientes, equipoEditando, errores, onGuardar, onCancelar)
//   PanelEquipos -> ListadoEquipos -> FilaEquipo   (equipos filtrados, onEditar, onEliminar, onCambiarEstado)
import { useEffect, useState } from 'react'
import api from '../api.js'
import ResumenEquipos from './ResumenEquipos.jsx'
import BuscadorEquipos from './BuscadorEquipos.jsx'
import FormularioEquipo from './FormularioEquipo.jsx'
import ListadoEquipos from './ListadoEquipos.jsx'
import AvisoPanel from './AvisoPanel.jsx'

function PanelEquipos() {
  // Datos que llegan de la API y estados de la petición
  const [equipos, setEquipos] = useState([])
  const [productos, setProductos] = useState([])
  const [clientes, setClientes] = useState([])
  const [cargando, setCargando] = useState(true)
  const [error, setError] = useState(null)
  // Estado de la interfaz: búsqueda, último aviso { id, texto }, equipo que se está editando y errores 400 del formulario
  const [busqueda, setBusqueda] = useState('')
  const [aviso, setAviso] = useState(null)
  const [seleccionado, setSeleccionado] = useState(null)
  const [errores, setErrores] = useState({})
  const [guardando, setGuardando] = useState(false)
  const [version, setVersion] = useState(0) // sube tras guardar: cambia la key del formulario y lo deja vacío

  // GET una sola vez al montar el panel: equipos, productos y clientes (para los desplegables del formulario)
  useEffect(() => {
    async function cargarDatos() {
      try {
        const [respEquipos, respProductos, respClientes] = await Promise.all([
          api.get('/equipos/'),
          api.get('/productos/'),
          api.get('/clientes/'),
        ])
        setEquipos(respEquipos.data)
        setProductos(respProductos.data)
        setClientes(respClientes.data)
      } catch (err) {
        console.error('Error al pedir los datos del panel:', err.message)
        setError('No se pudo cargar la lista de equipos')
      } finally {
        setCargando(false)
      }
    }
    cargarDatos()
  }, [])

  // Búsqueda: se filtra por número de serie ANTES de entregar los equipos al listado (sin tocar el original)
  const texto = busqueda.trim().toLowerCase()
  const equiposFiltrados = equipos.filter((e) => e.numero_serie.toLowerCase().includes(texto))

  function avisar(mensaje) {
    setAviso({ id: Date.now(), texto: mensaje }) // id nuevo = el AvisoPanel se vuelve a montar
  }

  // Eliminar: todavía solo cambia el estado de React (se conecta a DELETE en el Ejercicio 12)
  function eliminarEquipo(id) {
    const equipo = equipos.find((e) => e.id === id)
    setEquipos(equipos.filter((e) => e.id !== id))
    avisar(`Equipo ${equipo.numero_serie} eliminado`)
  }

  // Cambiar estado: PATCH con solo el campo que cambia; el estado se actualiza con map() cuando la API responde 200
  async function cambiarEstado(id) {
    const equipo = equipos.find((e) => e.id === id)
    const nuevoEstado = equipo.estado === 'OPERATIVO' ? 'MANTENIMIENTO' : 'OPERATIVO'
    try {
      const respuesta = await api.patch(`/equipos/${id}/`, { estado: nuevoEstado })
      setEquipos(equipos.map((e) => (e.id === id ? respuesta.data : e)))
      avisar(`Equipo ${equipo.numero_serie}: ahora ${nuevoEstado}`)
    } catch {
      avisar(`No se pudo cambiar el estado de ${equipo.numero_serie}`)
    }
  }

  // Editar: el padre guarda el equipo seleccionado y el formulario se llena con sus datos
  function editarEquipo(id) {
    setSeleccionado(equipos.find((e) => e.id === id))
    setErrores({})
  }

  function cancelarEdicion() {
    setSeleccionado(null)
    setErrores({})
  }

  // Alta (POST) o edición (PATCH) según haya un equipo seleccionado. El formulario solo entrega los datos.
  async function guardarEquipo(datos) {
    setGuardando(true)
    setErrores({})
    try {
      if (seleccionado) {
        const respuesta = await api.patch(`/equipos/${seleccionado.id}/`, datos) // 200
        setEquipos(equipos.map((e) => (e.id === seleccionado.id ? respuesta.data : e))) // arreglo NUEVO con map()
        avisar(`Equipo ${respuesta.data.numero_serie} actualizado`)
        setSeleccionado(null)
      } else {
        const respuesta = await api.post('/equipos/', datos) // 201
        setEquipos([...equipos, respuesta.data]) // arreglo NUEVO con lo que devolvió la API (trae el id real)
        avisar(`Equipo ${respuesta.data.numero_serie} agregado`)
      }
      setVersion(version + 1)
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setErrores(err.response.data) // { campo: ["mensaje"] } enviado por el serializer
      } else {
        setErrores({ general: ['No se pudo guardar el equipo. Intente de nuevo.'] })
      }
    } finally {
      setGuardando(false)
    }
  }

  // Estados de la petición: mientras carga o si falla, no se dibuja el resto del panel
  if (cargando) return <p className="aviso">Cargando equipos...</p>
  if (error) return <p className="error">{error}</p>

  return (
    <div>
      <ResumenEquipos equipos={equipos} />
      {aviso && <AvisoPanel key={aviso.id} texto={aviso.texto} />}
      <FormularioEquipo
        key={`${seleccionado ? seleccionado.id : 'nuevo'}-${version}`}
        productos={productos}
        clientes={clientes}
        equipoEditando={seleccionado}
        errores={errores}
        guardando={guardando}
        onGuardar={guardarEquipo}
        onCancelar={cancelarEdicion}
      />
      <BuscadorEquipos valor={busqueda} onCambiar={setBusqueda} />
      <ListadoEquipos
        equipos={equiposFiltrados}
        busqueda={busqueda}
        onEditar={editarEquipo}
        onEliminar={eliminarEquipo}
        onCambiarEstado={cambiarEstado}
      />
    </div>
  )
}

export default PanelEquipos
