# Laboratorio 13 — Ejercicio 2: Identificar módulos y roles

> La semana de cada módulo (S14, S15 y S16) es una **distribución propuesta**, porque el enunciado no detalla qué se implementa en cada una. Se puede ajustar según el temario del curso.

## Mapa de módulos de la cafetería en línea

| Módulo | Qué resuelve | Semana |
|---|---|---|
| Catálogo | Lista y detalle de productos y categorías | S14 |
| Inventario | Stock por producto; se descuenta al vender | S14 |
| Carrito | Productos que el cliente va eligiendo antes de comprar | S15 |
| Pedidos | Pedido (cabecera) y detalle; sus estados | S15 |
| Pagos | Cobro con pasarela externa; sin manejar datos de tarjeta | S15 |
| Usuarios y roles | Registro, inicio de sesión y roles | S16 |
| Seguridad | Autenticación, permisos y validación en el servidor | S16 |
| Notificaciones | Correos de confirmación y cambios de estado | S16 |
| Panel administrativo | Gestión de productos, stock y pedidos | S16 |

Ya construido en las semanas 3 a 12: apps y modelos de Django, API REST con DRF, CORS, React con Axios, componentes con props y estado, y el panel de ejemplo de equipos instalados (se reutiliza la idea del panel para la cafetería).

## Roles

| Rol | Qué puede hacer | Pantalla que usa |
|---|---|---|
| Visitante (sin sesión) | Ver el catálogo y el detalle de un producto; registrarse o iniciar sesión. No puede comprar. | Catálogo (`/productos`), detalle (`/productos/:id`), registro y login |
| Cliente (con sesión) | Todo lo del visitante, más agregar productos al carrito, confirmar el pedido, pagarlo y consultar sus pedidos anteriores. | Carrito (`/carrito`), pago (`/pago`), mis pedidos (`/mis-pedidos`) |
| Administrador | Crear, editar y eliminar productos y categorías; controlar el stock; ver todos los pedidos y cambiar su estado; consultar clientes. | Panel administrativo (`/admin/productos`, `/admin/pedidos`) |

## Capturas

- `01_mapa_modulos.png` — mapa de módulos por semana.
- `02_tabla_modulos.png` — tabla de módulos.
- `03_tabla_roles.png` — tabla de roles.
