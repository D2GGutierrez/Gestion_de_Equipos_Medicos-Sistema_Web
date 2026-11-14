// Fila del listado: recibe UN equipo y tres funciones por props. NO modifica la lista:
// cuando el usuario hace clic, AVISA al padre con onEditar(id), onEliminar(id) u onCambiarEstado(id).
// Lab 12 Ej 12: Eliminar pide confirmación con un segundo clic. Ese paso es solo de pantalla y vive en la fila.
import { useState } from 'react'

function FilaEquipo({ equipo, onEditar, onEliminar, onCambiarEstado }) {
  const [confirmando, setConfirmando] = useState(false)

  function confirmarEliminar() {
    setConfirmando(false)
    onEliminar(equipo.id) // recién ahora se avisa al padre, que hace el DELETE
  }

  return (
    <li className="tarjeta fila-equipo">
      <strong>{equipo.numero_serie}</strong> — {equipo.producto_nombre}
      <span className={`estado estado-${equipo.estado.toLowerCase()}`}>{equipo.estado}</span>
      <div className="detalle">
        {equipo.cliente_razon_social} · instalado el {equipo.fecha_instalacion} · garantía hasta {equipo.fin_garantia}
      </div>
      <div className="acciones">
        {confirmando ? (
          <>
            <span className="pregunta">¿Eliminar {equipo.numero_serie}? Esta acción no se puede deshacer.</span>
            <button className="boton-quitar" onClick={confirmarEliminar}>
              Confirmar
            </button>
            <button className="boton-cancelar-fila" onClick={() => setConfirmando(false)}>
              Cancelar
            </button>
          </>
        ) : (
          <>
            <button className="boton-accion" onClick={() => onCambiarEstado(equipo.id)}>
              {equipo.estado === 'OPERATIVO' ? 'Poner en mantenimiento' : 'Marcar operativo'}
            </button>
            <button className="boton-editar" onClick={() => onEditar(equipo.id)}>
              Editar
            </button>
            <button className="boton-quitar" onClick={() => setConfirmando(true)}>
              Eliminar
            </button>
          </>
        )}
      </div>
    </li>
  )
}

export default FilaEquipo
