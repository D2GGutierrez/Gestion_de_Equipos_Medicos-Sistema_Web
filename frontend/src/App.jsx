// Ejercicio 4 - Primer JSX con expresiones { }
const nombreApp = 'Gestión de Equipos Médicos'
const equipo = 'Monitor de Signos Vitales'
const precioBase = 4500
const IGV = 0.18

function precioConImpuesto(precio) {
  return precio * (1 + IGV)
}

function App() {
  return (
    <div>
      <h1>{nombreApp}</h1>
      <p>Equipo: {equipo}</p>
      <p>Precio base: S/ {precioBase.toFixed(2)}</p>
      <p>Precio con IGV (18%): S/ {precioConImpuesto(precioBase).toFixed(2)}</p>
      <p>Garantía de 2 años = {2 * 12} meses</p>
    </div>
  )
}

export default App
