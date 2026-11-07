// Semana 10 - Ejercicio 1: los datos viven en src/datos.js; src/components/ está listo para los componentes
import './App.css'
import { productos, clientes } from './datos.js'

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
      {/* && : mensaje de lista vacía también para la segunda lista */}
      {clientes.length === 0 && <p className="vacio">No hay clientes registrados</p>}

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
