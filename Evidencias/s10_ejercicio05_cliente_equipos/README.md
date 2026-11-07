# Laboratorio 10 – Ejercicio 5: Cliente con sus equipos (ClienteCard + EquipoItem)

## Qué se hizo
- `EquipoItem` (`src/components/EquipoItem.jsx`): muestra un equipo. Props: `serie`, `producto`, `estado`, `precio`.
- `ClienteCard` (`src/components/ClienteCard.jsx`): muestra un cliente. Props: `razonSocial` y `equipos`. Recorre `equipos` con `map()` (`key = e.id`) creando un `EquipoItem` por cada uno y **calcula** el total (`reduce` + `Number`) y la cantidad de equipos.
- `App.jsx` solo hace `clientes.map(...)` → `<ClienteCard key={c.id} razonSocial={c.razon_social} equipos={c.equipos} />`. La función `totalCliente` salió de `App` y su lógica quedó dentro de `ClienteCard`.

## Correspondencia API → props
| Campo de la API | Prop |
|---|---|
| `razon_social` | `razonSocial` |
| `equipos` | `equipos` |
| `numero_serie` | `serie` |
| `producto_nombre` | `producto` |
| `estado` | `estado` |
| `precio_base` | `precio` |

## ¿Por qué las props no se deben modificar?
Las props son de **solo lectura**: pertenecen al componente padre, que es quien es dueño de los datos. Un hijo que las cambiara haría que los datos fluyan en dos direcciones y la pantalla dejaría de ser predecible (el mismo dato diría cosas distintas en dos lugares). Si algo debe cambiar, se **calcula** a partir de las props (como el total) o se guarda en un **estado** propio (`useState`, Ejercicio 6).

### Prueba del error
Se probó temporalmente `props.razonSocial = 'Nombre cambiado'` dentro de `ClienteCard`. React congela el objeto `props` y el navegador muestra:

`Uncaught TypeError: Cannot assign to read only property 'razonSocial' of object '#<Object>'`

La pantalla queda en blanco. Luego se **revirtió** el cambio; el código entregado no modifica las props.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente.
- Consola del navegador sin errores ni warnings (la `key` está bien puesta en ambas listas).
- 3 clientes y 6 equipos mostrados; totales: 32801.25, 64000.00 y 6.50.

## Capturas
- Código: `captura_codigo_EquipoItem.jsx.png`, `captura_codigo_ClienteCard.jsx.png`, `captura_codigo_App.jsx.png`
- Navegador: `captura_pagina_antes.png` (Ej. 4), `captura_pagina_resultado.png` (Ej. 5)
- Error al mutar props: `captura_error_props_consola.png`, `captura_error_props_pantalla_en_blanco.png`
