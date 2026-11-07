// Ejercicio 10 (investigación) - Componente de relación: un Proveedor y, dentro, sus Suministros
// (un componente dentro de otro). "contacto" tiene valor por defecto.
import SuministroItem from './SuministroItem.jsx'

function ProveedorCard({ nombre, ruc, contacto = 'Sin contacto', telefono, suministros }) {
  return (
    <li className="tarjeta">
      <strong>{nombre}</strong> · RUC {ruc}
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
