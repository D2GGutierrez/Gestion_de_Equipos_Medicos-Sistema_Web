// Resumen (hermano del listado): recibe los equipos por props y calcula DATOS DERIVADOS sin useState.
// Si el padre cambia el arreglo (alta, eliminar, cambiar estado), este componente se redibuja y recalcula solo.
function ResumenEquipos({ equipos }) {
  // Conteo por estado con una sola pasada de reduce()
  const conteo = equipos.reduce((acc, e) => ({ ...acc, [e.estado]: (acc[e.estado] ?? 0) + 1 }), {})
  const operativos = conteo.OPERATIVO ?? 0
  const porcentaje = equipos.length === 0 ? 0 : Math.round((operativos / equipos.length) * 100)

  return (
    <div className="resumen">
      <div><strong>{equipos.length}</strong> equipos</div>
      <div className="estado estado-operativo">{operativos} operativos</div>
      <div className="estado estado-mantenimiento">{conteo.MANTENIMIENTO ?? 0} en mantenimiento</div>
      <div className="estado estado-inactivo">{conteo.INACTIVO ?? 0} inactivos</div>
      <div>{porcentaje}% operativos</div>
    </div>
  )
}

export default ResumenEquipos
