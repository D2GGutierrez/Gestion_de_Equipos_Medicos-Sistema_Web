# Laboratorio 12 — Ejercicio 9: Identificar el recurso del panel y sus operaciones

## Tabla de equivalencias con el proyecto

| Concepto trabajado en clase | Equivalente en el panel administrativo |
|---|---|
| Listar productos con `GET /api/productos/` | `GET /api/equipos/` — lista de **EquipoInstalado**, la entidad principal del panel |
| Estados de carga y de error | Los mismos tres estados en el listado del panel (cargando, error con Django apagado, lista vacía) |
| POST con el error 400 de `validate_precio` | POST del formulario de alta; la regla `validate_numero_serie` del serializer devuelve 400 |
| DELETE que responde 204 | `DELETE /api/equipos/<id>/` y actualización de la lista en pantalla |

## Datos del recurso

| Dato | Valor |
|---|---|
| Entidad principal | `EquipoInstalado` (equipos médicos instalados en clientes) |
| URL de la API | `/api/equipos/` y `/api/equipos/<id>/` (ViewSet con router, `ModelViewSet`) |
| Campos | `id`, `numero_serie` (único), `fecha_instalacion`, `fin_garantia`, `estado` (OPERATIVO / MANTENIMIENTO / INACTIVO), `producto` (FK), `cliente` (FK); de solo lectura: `producto_nombre`, `cliente_razon_social` |
| Regla de validación para probar el 400 | `validate_numero_serie`: formato `AAA-0000` (2 a 4 letras mayúsculas, guion y 4 dígitos; se normaliza a mayúsculas) y sin repetirse. Además `validate()` rechaza una garantía que termine antes de la instalación |
| Filtros | `?search=` (número de serie, nombre del producto, razón social del cliente), `?ordering=` (`id`, `numero_serie`, `fecha_instalacion`, `fin_garantia`; con `-` es descendente), `?estado=`, `?cliente=<id>`, `?producto=<id>`; se pueden combinar con `&` |
| Operaciones del panel | Listar (GET), crear (POST), editar (PATCH o PUT) y eliminar (DELETE) |

## Qué faltaba en la API y se agregó

La API de la Semana 8 **no tenía** endpoint REST de equipos (solo existían categorías, clientes, tickets y el listado de solo lectura `clientes-equipos`), y el serializer no tenía regla de validación propia. Se agregó, siguiendo la indicación del enunciado:

- `EquipoInstaladoViewSet` en `inventario/views/equipos.py`, registrado en el router de `inventario/urls.py` (`/api/equipos/`).
- `validate_numero_serie` y `validate()` en `EquipoInstaladoSerializer` (`inventario/serializer.py`).
- 10 pruebas nuevas en `inventario/tests_api.py` (200, 201, 400 por formato, 400 por serie repetida, 400 por fechas, PATCH, 404, 204 y filtros). Toda la suite pasa: 48 pruebas OK.

## Pruebas (con la API en marcha)

| Petición | Código | Resultado |
|---|---|---|
| `GET /api/equipos/` | 200 | 14 equipos |
| `GET /api/equipos/?search=monitor` | 200 | 6 equipos |
| `GET /api/equipos/?estado=MANTENIMIENTO` | 200 | 3 equipos |
| `GET /api/equipos/?estado=OPERATIVO&search=MON` | 200 | 4 equipos (combinando con `&`) |
| `GET /api/equipos/?ordering=-fecha_instalacion` | 200 | primero: MON-0201 (2026-10-05) |
| `POST` con serie `ABC` | 400 | `{"numero_serie":["El número de serie debe tener el formato AAA-0000 (2 a 4 letras, guion y 4 dígitos)."]}` |
| `POST` con serie repetida `eco-0001` | 400 | `{"numero_serie":["Ya existe un equipo con ese número de serie."]}` |
| `POST` con garantía antes de la instalación | 400 | `{"fin_garantia":["El fin de garantía no puede ser anterior a la fecha de instalación."]}` |

## Nota para los siguientes ejercicios

El formulario de alta necesita las listas de productos y clientes para sus desplegables. Clientes ya existe en la API (`/api/clientes/`); de productos no hay endpoint REST todavía, así que se agregará de solo lectura cuando se conecte el formulario (Ejercicio 11).

## Capturas

- `01_navegador_api_equipos.png` — la API de equipos con `?search=monitor&estado=OPERATIVO` en el navegador.
- `02_terminal_pruebas_api.png` — peticiones, códigos y respuestas 400.
- `03_codigo_serializer.png`, `04_codigo_viewset.png` — código agregado.
- `05_tests_django.png` — resultado de `python manage.py test inventario`.
