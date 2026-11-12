// Aviso temporal: muestra "Agregado: <nombre>" y desaparece solo a los 3 segundos.
// Efecto con [] = se ejecuta al MONTAR; la función que devuelve (limpieza) se ejecuta al DESMONTAR.
// Practica lo vuelve a montar con una key nueva cada vez que se agrega un producto.
import { useEffect, useState } from 'react'

function Aviso({ nombre }) {
  const [visible, setVisible] = useState(true)

  useEffect(() => {
    const temporizador = setTimeout(() => setVisible(false), 3000) // a los 3 s se oculta
    console.log('Aviso montado: temporizador de 3 s iniciado')
    return () => {
      clearTimeout(temporizador) // limpieza: evita que el temporizador siga vivo si el aviso se desmonta antes
      console.log('Aviso: temporizador limpiado')
    }
  }, [])

  return visible ? <p className="aviso">Agregado: {nombre}</p> : null
}

export default Aviso
