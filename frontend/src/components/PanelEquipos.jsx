// Lab 12 Ej 10 a 13: los datos vienen de la API de Django (GET con useEffect); el alta, la edición y la eliminación se envían con POST, PATCH y DELETE;
// la búsqueda y el filtro por estado viajan como parámetros (?search= y ?estado=) y el listado se recarga cuando cambian.
// PADRE del panel: el estado vive AQUÍ (estado elevado) y se entrega a los hijos por props.
// Los datos bajan por props y los avisos suben por las funciones que este componente define:
//   PanelEquipos -> ResumenEquipos                 (equipos)                      [hermano del listado]
//   PanelEquipos -> BuscadorEquipos / FiltroEstado (valor, onCambiar)
//   PanelEquipos -> FormularioEquipo               (productos, clientes, equipoEditando, errores, onGuardar, onCancelar)
//   PanelEquipos -> ListadoEquipos -> FilaEquipo   (equipos filtrados, onEditar, onEliminar, onCambiarEstado)
import { useEffect, useState } from 'react'
import api from '../api.js'
import ResumenEquipos from './ResumenEquipos.jsx'
import BuscadorEquipos from './BuscadorEquipos.jsx'
import FiltroEstado from './FiltroEstado.jsx'
import FormularioEquipo from './FormularioEquipo.jsx'
import ListadoEquipos from './ListadoEquipos.jsx'
import AvisoPanel from './AvisoPanel.jsx'

function PanelEquipos() {
  // Datos que llegan de la API y estados de la petición
  const [equipos, setEquipos] = useState([])
  const [productos, setProductos] = useState([])
  const [clientes, setClientes] = useState([])
  const [cargando, setCargando] = useState(true) // catálogos (productos y clientes)
  const [error, setError] = useState(null)
  const [cargandoLista, setCargandoLista] = useState(true) // listado de equipos (se repite en cada búsqueda o filtro)
  const [errorLista, setErrorLista] = useState(null)
  // Estado de la interfaz: búsqueda, filtro por estado, último aviso { id, texto }, equipo que se está editando y errores 400 del formulario
  const [busqueda, setBusqueda] = useState('')
  const [filtroEstado, setFiltroEstado] = useState('')
  const [aviso, setAviso] = useState(null)
  const [seleccionado, setSeleccionado] = useState(null)
  const [errores, setErrores] = useState({})
  const [guardando, setGuardando] = useState(false)
  const [version, setVersion] = useState(0) // sube tras guardar: cambia la key del formulario y lo deja vacío

  // GET una sola vez al montar el panel: productos y clientes (para los desplegables del formulario)
  useEffect(() => {
    async function cargarCatalogos() {
      try {
        const [respProductos, respClientes] = await Promise.all([api.get('/productos/'), api.get('/clientes/')])
        setProductos(respProductos.data)
        setClientes(respClientes.data)
      } catch (err) {
        console.error('Error al pedir los datos del panel:', err.message)
        setError('No se pudo cargar el panel')
      } finally {
        setCargando(false)
      }
    }
    cargarCatalogos()
  }, [])

  // GET de los equipos con parámetros: se vuelve a ejecutar cada vez que cambia la búsqueda o el filtro.
  // Solo se envían los parámetros que tienen valor: /equipos/?search=MON&estado=OPERATIVO
  useEffect(() => {
    const controlador = new AbortController() // permite cancelar la petición pendiente
    async function cargarEquipos() {
      setCargandoLista(true)
      setErrorLista(null)
      const params = {}
      if (busqueda.trim() !== '') params.search = busqueda.trim()
      if (filtroEstado !== '') params.estado = filtroEstado
      try {
        const respuesta = await api.get('/equipos/', { params, signal: controlador.signal })
        setEquipos(respuesta.data)
      } catch (err) {
        if (err.code === 'ERR_CANCELED') return // la petición se canceló a propósito: no es un error
        console.error('Error al pedir los equipos:', err.message)
        setErrorLista('No se pudo cargar la lista de equipos')
      } finally {
        if (!controlador.signal.aborted) setCargandoLista(false)
      }
    }
    cargarEquipos()
    return () => controlador.abort() // limpieza: si cambia el filtro antes de la respuesta, se cancela la anterior
  }, [busqueda, filtroEstado])

  // Texto que describe los filtros activos (para el mensaje de «sin resultados»)
  const filtrosActivos = [busqueda.trim(), filtroEstado && `estado ${filtroEstado}`].filter(Boolean).join(' + ')

  function avisar(mensaje, tipo = 'exito') {
    setAviso({ id: Date.now(), texto: mensaje, tipo }) // id nuevo = el AvisoPanel se vuelve a montar
  }

  // Eliminar (la confirmación ya la pidió la fila): DELETE y, según la respuesta, se actualiza el estado
  async function eliminarEquipo(id) {
    const equipo = equipos.find((e) => e.id === id)
    try {
      await api.delete(`/equipos/${id}/`) // 204 No Content
      setEquipos(equipos.filter((e) => e.id !== id)) // arreglo NUEVO sin el equipo eliminado
      avisar(`Equipo ${equipo.numero_serie} eliminado`)
    } catch (err) {
      if (err.response && err.response.status === 404) {
        // 404: el registro ya no existe en el servidor (alguien lo borró antes); la lista se pone al día
        setEquipos(equipos.filter((e) => e.id !== id))
        avisar(`El equipo ${equipo.numero_serie} ya no existe en el servidor (404). Se quitó de la lista.`, 'error')
      } else {
        avisar(`No se pudo eliminar el equipo ${equipo.numero_serie}`, 'error')
      }
    }
    if (seleccionado && seleccionado.id === id) setSeleccionado(null) // si se estaba editando, se cierra la edición
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
  if (cargando) return <p className="aviso">Cargando panel...</p>
  if (error) return <p className="error">{error}</p>

  return (
    <div>
      <ResumenEquipos equipos={equipos} />
      {aviso && <AvisoPanel key={aviso.id} texto={aviso.texto} tipo={aviso.tipo} />}
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
      <div className="barra-filtros">
        <BuscadorEquipos valor={busqueda} onCambiar={setBusqueda} />
        <FiltroEstado valor={filtroEstado} onCambiar={setFiltroEstado} />
      </div>
      {cargandoLista && <p className="aviso">Cargando equipos...</p>}
      {errorLista && <p className="error">{errorLista}</p>}
      {!cargandoLista && !errorLista && (
        <ListadoEquipos
          equipos={equipos}
          busqueda={filtrosActivos}
          onEditar={editarEquipo}
          onEliminar={eliminarEquipo}
          onCambiarEstado={cambiarEstado}
        />
      )}
    </div>
  )
}

export default PanelEquipos
