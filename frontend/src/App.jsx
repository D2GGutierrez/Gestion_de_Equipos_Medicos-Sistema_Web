// Ejercicio 5 - Lista con map() y key
// Misma forma que la respuesta de la API de la Semana 8 (GET /api/productos/):
// los decimales llegan como TEXTO ("4500.00"), no como número.
const productos = [
  { id: 1, codigo_sku: 'ECO-100', nombre: 'Ecógrafo Doppler Color', marca: 'GE', modelo: 'Logiq P9', precio_base: '18500.00', meses_garantia: 24, stock: 3, categoria: { id: 1, nombre: 'Diagnóstico por Imagen' } },
  { id: 2, codigo_sku: 'MON-200', nombre: 'Monitor de Signos Vitales', marca: 'Philips', modelo: 'IntelliVue MX450', precio_base: '4500.5', meses_garantia: 12, stock: 8, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
  { id: 3, codigo_sku: 'VEN-300', nombre: 'Ventilador Mecánico', marca: 'Dräger', modelo: 'Evita V300', precio_base: '32000.00', meses_garantia: 24, stock: 2, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 4, codigo_sku: 'DES-400', nombre: 'Desfibrilador Bifásico', marca: 'Zoll', modelo: 'R Series', precio_base: '9800.75', meses_garantia: 18, stock: 0, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 5, codigo_sku: 'OXI-500', nombre: 'Oxímetro de Pulso', marca: 'Masimo', modelo: 'Rad-97', precio_base: '6.5', meses_garantia: 6, stock: 25, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
]

function App() {
  return (
    <div>
      <h1>Gestión de Equipos Médicos</h1>
      <h2>Productos ({productos.length})</h2>
      <ul>
        {productos.map((p) => (
          <li key={p.id}>
            <strong>{p.nombre}</strong> — {p.marca} {p.modelo} · {p.categoria.nombre} ·
            S/ {Number(p.precio_base).toFixed(2)} · Stock: {p.stock}
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
