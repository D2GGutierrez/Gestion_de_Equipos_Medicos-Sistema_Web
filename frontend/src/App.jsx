// Semana 10 - Ejercicios 1 a 8 y 10 (investigación): datos en src/datos.js y componentes en src/components/
import './App.css'
import { productos, clientes } from './datos.js'
import ProductoCard from './components/ProductoCard.jsx'
import ListaProductos from './components/ListaProductos.jsx'
import Tarjeta from './components/Tarjeta.jsx'
import ClienteCard from './components/ClienteCard.jsx'
import ListaProveedores from './components/ListaProveedores.jsx'
import { proveedores } from './datosInvestigacion.js'

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
        {clientes.length === 0 && <p className="vacio">No hay clientes registrados</p>}
        {/* ClienteCard recibe razonSocial y equipos; dentro usa EquipoItem por cada equipo */}
        <ul className="lista">
          {clientes.map((c) => (
            <ClienteCard key={c.id} razonSocial={c.razon_social} equipos={c.equipos} />
          ))}
        </ul>
      </Tarjeta>

      {/* Investigación propia: Proveedor -> Suministro (modelo intermedio del ManyToMany) */}
      <Tarjeta titulo="Investigación: proveedores y sus suministros">
        <ListaProveedores proveedores={proveedores} />
      </Tarjeta>
    </div>
  )
}

export default App
