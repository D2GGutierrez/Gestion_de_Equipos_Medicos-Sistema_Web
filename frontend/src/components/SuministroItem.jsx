// Ejercicio 10 (investigación) - Una fila del modelo intermedio Suministro (Producto <-> Proveedor).
// Campos de la API -> props: producto_nombre -> producto, precio_compra -> precio, dias_entrega_promedio -> dias,
// es_proveedor_principal -> principal (valor por defecto false).
function SuministroItem({ producto, precio, dias, principal = false }) {
  return (
    <li>
      {producto} — S/ {Number(precio).toFixed(2)} · entrega en {dias} {dias === 1 ? 'día' : 'días'}
      {principal && <strong className="principal"> ★ Proveedor principal</strong>}
    </li>
  )
}

export default SuministroItem
