// Ejercicios 5 a 8 - Lista con map()/key, renderizado condicional, listas anidadas y estilos
import './App.css'
// Misma forma que la respuesta de la API de la Semana 8 (GET /api/productos/):
// los decimales llegan como TEXTO ("4500.00"), no como número.
const productos = [
  { id: 1, codigo_sku: 'ECO-100', nombre: 'Ecógrafo Doppler Color', marca: 'GE', modelo: 'Logiq P9', precio_base: '18500.00', meses_garantia: 24, stock: 3, categoria: { id: 1, nombre: 'Diagnóstico por Imagen' } },
  { id: 2, codigo_sku: 'MON-200', nombre: 'Monitor de Signos Vitales', marca: 'Philips', modelo: 'IntelliVue MX450', precio_base: '4500.5', meses_garantia: 12, stock: 8, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
  { id: 3, codigo_sku: 'VEN-300', nombre: 'Ventilador Mecánico', marca: 'Dräger', modelo: 'Evita V300', precio_base: '32000.00', meses_garantia: 24, stock: 2, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 4, codigo_sku: 'DES-400', nombre: 'Desfibrilador Bifásico', marca: 'Zoll', modelo: 'R Series', precio_base: '9800.75', meses_garantia: 18, stock: 0, categoria: { id: 3, nombre: 'Soporte Vital' } },
  { id: 5, codigo_sku: 'OXI-500', nombre: 'Oxímetro de Pulso', marca: 'Masimo', modelo: 'Rad-97', precio_base: '6.5', meses_garantia: 6, stock: 25, categoria: { id: 2, nombre: 'Monitoreo de Pacientes' } },
]

// Relación 1:N (Cliente -> equipos instalados), con la forma de GET /api/clientes-equipos/.
// Cada cliente trae un arreglo "equipos" dentro; los decimales llegan como texto.
const clientes = [
  {
    id: 1, razon_social: 'Clínica San Gabriel S.A.',
    equipos: [
      { id: 11, numero_serie: 'ECO-0001', estado: 'OPERATIVO', producto_nombre: 'Ecógrafo Doppler Color', precio_base: '18500.00' },
      { id: 12, numero_serie: 'MON-0101', estado: 'OPERATIVO', producto_nombre: 'Monitor de Signos Vitales', precio_base: '4500.5' },
      { id: 13, numero_serie: 'DES-0302', estado: 'MANTENIMIENTO', producto_nombre: 'Desfibrilador Bifásico', precio_base: '9800.75' },
    ],
  },
  {
    id: 2, razon_social: 'Hospital Regional de Arequipa',
    equipos: [
      { id: 21, numero_serie: 'VEN-0201', estado: 'OPERATIVO', producto_nombre: 'Ventilador Mecánico', precio_base: '32000.00' },
      { id: 22, numero_serie: 'VEN-0202', estado: 'MANTENIMIENTO', producto_nombre: 'Ventilador Mecánico', precio_base: '32000.00' },
    ],
  },
  {
    id: 3, razon_social: 'Centro Médico Santa Rosa E.I.R.L.',
    equipos: [
      { id: 31, numero_serie: 'OXI-0401', estado: 'INACTIVO', producto_nombre: 'Oxímetro de Pulso', precio_base: '6.5' },
    ],
  },
]

// Total por cliente: suma del precio de sus equipos (texto -> número con Number)
function totalCliente(cliente) {
  return cliente.equipos.reduce((suma, e) => suma + Number(e.precio_base), 0)
}

function App() {
  return (
    <div className="app">
      <h1 className="titulo">Gestión de Equipos Médicos</h1>
      <h2>Productos ({productos.length})</h2>

      {/* && : el mensaje solo aparece si el arreglo está vacío */}
      {productos.length === 0 && <p className="vacio">No hay registros</p>}

      <ul className="lista">
        {productos.map((p) => (
          <li key={p.id} className="tarjeta">
            <strong>{p.nombre}</strong> — {p.marca} {p.modelo} · {p.categoria.nombre} ·
            S/ {Number(p.precio_base).toFixed(2)} ·{' '}
            {/* ternario: una cosa u otra según el stock */}
            {p.stock > 0 ? `Stock: ${p.stock}` : <span className="agotado">Agotado</span>}
            {/* &&: solo se muestra si la condición es verdadera */}
            {p.stock > 0 && p.stock <= 3 && <em className="ultimas"> ¡Últimas unidades!</em>}
          </li>
        ))}
      </ul>

      <h2>Clientes y sus equipos instalados</h2>
      {/* map() EXTERNO: un <li> por cliente (key = id del cliente) */}
      <ul className="lista">
        {clientes.map((c) => (
          <li key={c.id} className="tarjeta">
            <strong>{c.razon_social}</strong> ({c.equipos.length} {c.equipos.length === 1 ? 'equipo' : 'equipos'})
            {/* map() INTERNO: un <li> por equipo del cliente (key = id del equipo) */}
            <ul className="equipos">
              {c.equipos.map((e) => (
                <li key={e.id}>
                  {e.numero_serie} — {e.producto_nombre} · {e.estado} · S/ {Number(e.precio_base).toFixed(2)}
                </li>
              ))}
            </ul>
            {/* style={{ }}: estilo en línea, un objeto JavaScript (propiedades en camelCase) */}
            <p style={{ fontWeight: 'bold', color: '#065f46' }}>Total de equipos: S/ {totalCliente(c).toFixed(2)}</p>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default App
