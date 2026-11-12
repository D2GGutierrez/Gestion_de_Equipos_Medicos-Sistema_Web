// Hermano de Catalogo: recibe las líneas del carrito por props y las muestra.
// No guarda nada: el carrito vive en el padre (Practica) y baja por props.
function Carrito({ lineas }) {
  return (
    <div>
      <h3>Carrito</h3>
      <ul className="lista">
        {lineas.map((l) => (
          <li key={l.id} className="tarjeta">
            <strong>{l.nombre}</strong> · S/ {Number(l.precio).toFixed(2)} × {l.cantidad}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default Carrito
