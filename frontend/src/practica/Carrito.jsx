// Hermano de Catalogo: recibe las líneas del carrito por props y las muestra.
// No guarda nada: el carrito vive en el padre (Practica) y baja por props.
function Carrito({ lineas }) {
  // Datos DERIVADOS: se calculan en cada renderizado a partir de las props, sin useState.
  // El precio llega como texto (como la API), por eso se convierte con Number().
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

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
      <p style={{ fontWeight: 'bold', color: '#065f46' }}>
        Unidades: {unidades} · Total: S/ {total.toFixed(2)}
      </p>
    </div>
  )
}

export default Carrito
