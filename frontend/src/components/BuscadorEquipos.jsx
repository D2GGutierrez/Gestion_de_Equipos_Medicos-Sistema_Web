// Buscador (hijo): campo CONTROLADO por el padre. Recibe "valor" y avisa cada cambio con onCambiar(texto).
function BuscadorEquipos({ valor, onCambiar }) {
  return (
    <input
      className="buscador"
      type="text"
      placeholder="Buscar por número de serie..."
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default BuscadorEquipos
