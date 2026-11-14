# Laboratorio 12 — Ejercicio 4: Solicitud GET con useEffect

## Código (`src/practica/ListaPractica.jsx`)

```jsx
import { useEffect, useState } from 'react'
import api from '../api.js'

function ListaPractica() {
  const [clientes, setClientes] = useState([])

  useEffect(() => {
    async function cargarClientes() {
      const respuesta = await api.get('/clientes/') // GET http://127.0.0.1:8000/api/clientes/
      setClientes(respuesta.data)
    }
    cargarClientes()
  }, [])

  return (
    <ul className="lista">
      {clientes.map((c) => (
        <li key={c.id}>
          <strong>{c.razon_social}</strong> — RUC {c.numero_identificacion} ({c.activo ? 'activo' : 'inactivo'})
        </li>
      ))}
    </ul>
  )
}
```

Se muestra en `App.jsx` dentro de la tarjeta «Laboratorio 12 - Práctica: clientes desde la API».

## Resultado

La página lista los 3 clientes que vienen de la base de datos de Django (ya no son datos escritos a mano). En la pestaña Network: **GET** `http://127.0.0.1:8000/api/clientes/` → **200 OK**, `application/json`, origen `http://localhost:5173` (permitido por CORS). La consola quedó sin errores ni advertencias, y `npm run lint` y `npm run build` terminan con código 0.

Nota: en desarrollo aparecen **dos** peticiones GET idénticas. No es un error: `React.StrictMode` monta, desmonta y vuelve a montar el componente para detectar efectos con fallas, así que el efecto corre dos veces. En producción (`npm run build`) corre una sola vez.

## Por qué la petición va dentro de useEffect

El cuerpo del componente se ejecuta en **cada render**. Si la petición estuviera ahí, `setClientes` provocaría otro render, que haría otra petición, y así en un bucle infinito de peticiones. Pedir datos es un efecto secundario (sale del mundo de React hacia el servidor), y `useEffect` con `[]` lo ejecuta una sola vez, después de que el componente se dibujó por primera vez.

## Por qué la función del efecto no es async

Una función `async` siempre devuelve una promesa, y React espera que el efecto devuelva `undefined` o una función de limpieza (por ejemplo, para cancelar un temporizador). Si le llega una promesa, la interpreta mal y avisa con una advertencia. Por eso el efecto es una función normal que declara adentro `async function cargarClientes()` y la llama; así se puede usar `await` sin romper el contrato del efecto.

## Capturas

- `01_codigo_ListaPractica.png` — código del componente.
- `02_pagina_lista.png` — la lista en el navegador.
- `03_network_get_200.png` — petición GET con código 200 (resumen de la pestaña Network).
