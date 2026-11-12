// Aviso temporal del panel: muestra un texto y desaparece solo a los 3 segundos.
// useEffect con [] = corre al MONTAR; su función de limpieza (clearTimeout) corre al DESMONTAR.
// El padre lo monta de nuevo con una key distinta en cada acción, así el temporizador empieza de cero.
import { useEffect, useState } from 'react'

function AvisoPanel({ texto }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const temporizador = setTimeout(() => setVisible(false), 3000)
    return () => clearTimeout(temporizador) // limpieza: evita un temporizador vivo si el aviso se desmonta antes
  }, [])

  return visible ? <p className="aviso">{texto}</p> : null
}

export default AvisoPanel
