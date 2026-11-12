// Fila del listado: recibe UN equipo y dos funciones por props. NO modifica la lista:
// cuando el usuario hace clic, AVISA al padre con onEliminar(id) u onCambiarEstado(id).
function FilaEquipo({ equipo, onEliminar, onCambiarEstado }) {
  return (
    <li className="tarjeta fila-equipo">
      <strong>{equipo.numero_serie}</strong> — {equipo.producto_nombre}
      <span className={`estado estado-${equipo.estado.toLowerCase()}`}>{equipo.estado}</span>
      <div className="detalle">
        {equipo.cliente_razon_social} · instalado el {equipo.fecha_instalacion} · garantía hasta {equipo.fin_garantia}
      </div>
      <div className="acciones">
        <button className="boton-accion" onClick={() => onCambiarEstado(equipo.id)}>
          {equipo.estado === 'OPERATIVO' ? 'Poner en mantenimiento' : 'Marcar operativo'}
        </button>
        <button className="boton-quitar" onClick={() => onEliminar(equipo.id)}>
          Eliminar
        </button>
      </div>
    </li>
  )
}

export default FilaEquipo
