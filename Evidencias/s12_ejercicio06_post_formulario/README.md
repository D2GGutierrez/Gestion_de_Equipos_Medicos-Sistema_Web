# Laboratorio 12 — Ejercicio 6: POST con un formulario controlado

## Código (`src/practica/ListaPractica.jsx`)

Formulario controlado (cada input tiene `value` y `onChange`) con un solo manejador que usa el atributo `name`:

```jsx
function cambiar(e) {
  setFormulario({ ...formulario, [e.target.name]: e.target.value })
}

async function enviar(e) {
  e.preventDefault()
  setEnviando(true)
  setErrores({})
  try {
    const respuesta = await api.post('/clientes/', formulario)   // POST -> 201
    setClientes([...clientes, respuesta.data])                   // arreglo NUEVO con lo que devolvió el servidor
    setFormulario(vacio)
  } catch (err) {
    if (err.response && err.response.status === 400) {
      setErrores(err.response.data)                              // { campo: ["mensaje"] } del serializer
    } else {
      setErrores({ general: ['No se pudo guardar el cliente'] })
    }
  } finally {
    setEnviando(false)
  }
}
```

Junto a cada input se muestran los mensajes de `errores[campo]`.

## Resultados (probados en el navegador)

| Prueba | Datos | Network | En pantalla |
|---|---|---|---|
| Datos válidos | RUC `20555666777` | **POST** `/api/clientes/` → **201 Created** | El cliente nuevo aparece en la lista sin recargar la página (de 3 a 4) |
| Datos que incumplen la regla | RUC `123` | **POST** `/api/clientes/` → **400 Bad Request** | «El RUC debe tener exactamente 11 dígitos.» bajo el campo RUC; la lista sigue con 3 |

Respuesta 400 recibida: `{"numero_identificacion":["El RUC debe tener exactamente 11 dígitos."]}` (regla `validate_numero_identificacion` del serializer de la Semana 8, que viaja en `err.response.data`).

El cliente de prueba se eliminó de la base después del ensayo. En la consola solo aparece la línea que el navegador imprime por toda respuesta 400 (`Failed to load resource: ... 400`); no hay advertencias de React. `npm run lint` y `npm run build` terminan con código 0.

## Por qué se agrega `respuesta.data` y no el formulario

El servidor es quien asigna el `id` (y valores por defecto como `activo`); la respuesta 201 trae el registro tal como quedó guardado, por eso se agrega ese y no los datos del formulario. Se usa un arreglo nuevo (`[...clientes, respuesta.data]`) porque React solo se redibuja si el estado cambia de referencia; `push` no lo notificaría.

## Capturas

- `01_antes.png`, `02_despues_201.png`, `03_error_400.png` — la página.
- `04_codigo_parte1.png`, `05_codigo_parte2.png` — código.
- `06_network_post_201.png`, `07_network_post_400.png` — pestaña Network (método, código, datos enviados y recibidos).
