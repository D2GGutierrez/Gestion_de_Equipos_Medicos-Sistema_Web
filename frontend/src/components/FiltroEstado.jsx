// Filtro por estado (hijo): select CONTROLADO por el padre. Avisa cada cambio con onCambiar(estado).
// "" significa "sin filtro": el padre no envía el parámetro ?estado= a la API.
function FiltroEstado({ valor, onCambiar }) {
  return (
    <select className="filtro-estado" value={valor} onChange={(e) => onCambiar(e.target.value)}>
      <option value="">Todos los estados</option>
      <option value="OPERATIVO">Operativo</option>
      <option value="MANTENIMIENTO">En mantenimiento</option>
      <option value="INACTIVO">Inactivo</option>
    </select>
  )
}

export default FiltroEstado
