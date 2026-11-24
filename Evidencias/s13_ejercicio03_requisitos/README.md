# Laboratorio 13 — Ejercicio 3: Redactar requisitos

## Requisitos funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RF-01 | El sistema muestra el catálogo de productos con nombre, precio y stock disponible. | Alta | `GET /api/productos/` responde 200 y la pantalla lista todos los productos activos. |
| RF-02 | El cliente puede agregar un producto al carrito y elegir la cantidad. | Alta | Al agregar 2 unidades de un producto de S/ 8,50, el carrito muestra cantidad 2 y subtotal S/ 17,00. |
| RF-03 | El cliente puede confirmar el carrito y el sistema crea un pedido con su detalle en estado «pendiente». | Alta | `POST /api/pedidos/` responde 201 y el pedido aparece en «Mis pedidos» con sus productos. |
| RF-04 | El sistema no permite pedir más unidades que el stock disponible. | Alta | Un pedido con cantidad mayor al stock responde 400 con mensaje claro y el stock no cambia. |
| RF-05 | El administrador puede crear, editar y eliminar productos desde el panel. | Media | POST responde 201, PATCH 200 y DELETE 204; la lista del panel se actualiza sin recargar. |

## Requisitos no funcionales

| ID | Descripción | Prioridad | Criterio de aceptación |
|---|---|---|---|
| RNF-01 | Rendimiento: el catálogo debe cargar rápido con un volumen normal de productos. | Media | Con 100 productos, el listado se muestra en menos de 2 segundos (medido en la pestaña Network). |
| RNF-02 | Seguridad de acceso: las operaciones de pedidos y del panel exigen sesión y rol adecuado. | Alta | Sin sesión la API responde 401; con rol cliente en rutas de administrador responde 403. |
| RNF-03 | Seguridad de pagos: el sistema nunca recibe ni guarda el número de tarjeta; solo la confirmación de la pasarela. | Alta | Ningún modelo ni petición de la API contiene campos de número de tarjeta o CVV. |
| RNF-04 | Usabilidad: la tienda debe poder usarse desde un celular. | Media | A 360 px de ancho, en Chrome, no hay desplazamiento horizontal y los botones se pueden presionar. |
| RNF-05 | Mantenibilidad: el código debe pasar las verificaciones del proyecto. | Media | `npm run lint`, `npm run build`, `python manage.py check` y las pruebas de la API terminan sin errores. |

## Diferencia entre requisitos funcionales y no funcionales

Un **requisito funcional** dice **qué hace** el sistema: una función concreta que el usuario puede ver o usar (mostrar el catálogo, agregar al carrito, crear un pedido). Un **requisito no funcional** dice **cómo debe comportarse** o **qué tan bien** debe hacerlo: rapidez, seguridad, facilidad de uso, mantenimiento. No añade una función nueva, sino una condición de calidad que el sistema debe cumplir mientras realiza sus funciones. Los dos se redactan con un criterio de aceptación para poder comprobarlos.

## Reescritura del requisito vago «El sistema debe ser rápido y seguro»

Está mal redactado porque «rápido» y «seguro» no tienen un valor que se pueda medir ni una prueba que se pueda hacer, y además junta dos ideas distintas en una sola frase. Se reescribe como dos requisitos verificables:

| Versión | Requisito | Prioridad | Cómo se verifica |
|---|---|---|---|
| Original (vago) | El sistema debe ser rápido y seguro. | — | No se puede medir ni probar. |
| RNF verificable 1 (rendimiento) | El listado de productos debe mostrarse en menos de 2 segundos con hasta 100 productos. | Media | Se mide en la pestaña Network: tiempo total de la petición y el dibujo < 2 s. |
| RNF verificable 2 (seguridad) | Crear, editar y eliminar productos solo debe permitirse a usuarios con rol administrador. | Alta | Sin sesión: 401. Con rol cliente: 403. Con rol administrador: 201, 200 y 204. |

## Capturas

- `01_requisitos_funcionales.png`, `02_requisitos_no_funcionales.png` — tablas de requisitos.
- `03_requisito_vago.png` — reescritura del requisito vago.
