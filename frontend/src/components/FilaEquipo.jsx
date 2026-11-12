// Fila del listado: recibe UN equipo por props y lo muestra. (Los botones de acción llegan en el Ejercicio 11.)
function FilaEquipo({ equipo }) {
  return (
    <li className="tarjeta fila-equipo">
      <strong>{equipo.numero_serie}</strong> — {equipo.producto_nombre}
      <span className={`estado estado-${equipo.estado.toLowerCase()}`}>{equipo.estado}</span>
      <div className="detalle">
        {equipo.cliente_razon_social} · instalado el {equipo.fecha_instalacion} · garantía hasta {equipo.fin_garantia}
      </div>
    </li>
  )
}

export default FilaEquipo
