// Semana 10 - Ejercicios 1 a 4: datos en src/datos.js y componentes en src/components/
  import './App.css'
  import { productos, clientes } from './datos.js'
  import ProductoCard from './components/ProductoCard.jsx'
  import ListaProductos from './components/ListaProductos.jsx'
  import Tarjeta from './components/Tarjeta.jsx'

  // Total por cliente: suma del precio de sus equipos (texto -> número con Number)
  function totalCliente(cliente) {
    return cliente.equipos.reduce((suma, e) => suma + Number(e.precio_base), 0)
  }

  function App() {
    return (
      <div className="app">
        <h1 className="titulo">Gestión de Equipos Médicos</h1>

        {/* Tarjeta: título por props y el contenido llega como children */}
        <Tarjeta titulo="Catálogo de productos">
          <ListaProductos productos={productos} />
      </Tarjeta>

      {/* Prueba del valor por defecto: este producto no envía la prop "marca" */}
      <Tarjeta titulo="Prueba del valor por defecto">
        <ul className="lista">
          <ProductoCard nombre="Equipo de prueba" modelo="X-1" categoria="Sin categoría" precio="120.5" stock={4} />
        </ul>
      </Tarjeta>

      <Tarjeta titulo="Clientes y sus equipos instalados">
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
      </Tarjeta>
    </div>
  )
}

export default App
