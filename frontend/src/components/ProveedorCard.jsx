// Ejercicio 10 (investigación) - Componente de relación: un Proveedor y, dentro, sus Suministros
// (un componente dentro de otro). "contacto" tiene valor por defecto.
// Ejercicio 11 - Botón con estado: marcar / quitar el proveedor de favoritos (useState + onClick).
import { useState } from 'react'
import SuministroItem from './SuministroItem.jsx'

function ProveedorCard({ nombre, ruc, contacto = 'Sin contacto', telefono, suministros }) {
  // Estado booleano propio de cada tarjeta: cada proveedor es favorito o no, de forma independiente
  const [favorito, setFavorito] = useState(false)

  return (
    <li className={favorito ? 'tarjeta favorito' : 'tarjeta'}>
      <strong>{nombre}</strong> · RUC {ruc}
      {favorito && <span className="pedido"> ★ Favorito</span>}
      <div className="acciones">
        {/* !favorito invierte el valor: true -> false, false -> true */}
        <button onClick={() => setFavorito(!favorito)}>
          {favorito ? 'Quitar de favoritos' : 'Marcar como favorito'}
        </button>
      </div>
      <div>
        Contacto: {contacto} · Tel. {telefono} · {suministros.length} {suministros.length === 1 ? 'producto suministrado' : 'productos suministrados'}
      </div>
      {suministros.length === 0 && <p className="vacio">Sin suministros registrados</p>}
      <ul className="equipos">
        {suministros.map((s) => (
          <SuministroItem
            key={s.id}
            producto={s.producto_nombre}
            precio={s.precio_compra}
            dias={s.dias_entrega_promedio}
            principal={s.es_proveedor_principal}
          />
        ))}
      </ul>
    </li>
  )
}

export default ProveedorCard
