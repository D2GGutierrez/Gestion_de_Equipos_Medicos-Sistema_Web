// Hermano de Catalogo: recibe las líneas del carrito por props y las muestra.
// No guarda nada: el carrito vive en el padre (Practica) y baja por props.
// Ejercicio 8: useEffect con [unidades] actualiza el título de la pestaña cuando cambia la cantidad.
// Para quitar o vaciar NO modifica la lista: AVISA al padre con onQuitar(id) y onVaciar().
import { useEffect } from 'react'

function Carrito({ lineas, onQuitar, onVaciar }) {
  // Datos DERIVADOS: se calculan en cada renderizado a partir de las props, sin useState.
  // El precio llega como texto (como la API), por eso se convierte con Number().
  const total = lineas.reduce((suma, l) => suma + Number(l.precio) * l.cantidad, 0)
  const unidades = lineas.reduce((suma, l) => suma + l.cantidad, 0)

  // Efecto: se ejecuta después de dibujar y SOLO cuando cambia "unidades" (arreglo de dependencias)
  useEffect(() => {
    document.title = `Carrito (${unidades}) — Cafetería`
    console.log('Efecto de Carrito: título actualizado, unidades =', unidades)
  }, [unidades])

  return (
    <div>
      <h3>Carrito</h3>
      {/* && : mensaje solo cuando no hay líneas */}
      {lineas.length === 0 && <p className="vacio">El carrito está vacío</p>}
      <ul className="lista">
        {lineas.map((l) => (
          <li key={l.id} className="tarjeta">
            <strong>{l.nombre}</strong> · S/ {Number(l.precio).toFixed(2)} × {l.cantidad}{' '}
            <button className="boton-quitar" onClick={() => onQuitar(l.id)}>Quitar</button>
          </li>
        ))}
      </ul>
      <p style={{ fontWeight: 'bold', color: '#065f46' }}>
        Unidades: {unidades} · Total: S/ {total.toFixed(2)}
      </p>
      {lineas.length > 0 && <button className="boton-quitar" onClick={onVaciar}>Vaciar carrito</button>}
    </div>
  )
}

export default Carrito
