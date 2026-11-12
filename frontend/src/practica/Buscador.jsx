// Hijo de Practica: campo de texto CONTROLADO. No guarda el texto: lo recibe en "valor"
// y avisa cada cambio al padre con onCambiar(texto).
function Buscador({ valor, onCambiar }) {
  return (
    <input
      className="buscador"
      type="text"
      placeholder="Buscar producto..."
      value={valor}
      onChange={(e) => onCambiar(e.target.value)}
    />
  )
}

export default Buscador
