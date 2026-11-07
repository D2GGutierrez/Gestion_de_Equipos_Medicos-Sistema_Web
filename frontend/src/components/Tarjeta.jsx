// Ejercicio 4 - Componente contenedor: recibe un título por props y el contenido por "children".
// Lo que se escribe ENTRE <Tarjeta> y </Tarjeta> llega en la prop children.
function Tarjeta({ titulo, children }) {
  return (
    <section className="panel">
      <h2 className="panel-titulo">{titulo}</h2>
      {children}
    </section>
  )
}

export default Tarjeta
