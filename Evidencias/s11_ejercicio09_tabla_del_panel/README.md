# Laboratorio 11 – Ejercicio 9: Identificar los componentes del panel

## Entidad principal elegida
**Equipo instalado** (`EquipoInstalado`), el corazón del proyecto *Gestión de Equipos Médicos*: cada registro es un equipo vendido e instalado en un cliente. La base de datos ya tiene 14 registros reales, que servirán de datos escritos a mano con la forma de la respuesta de la API de la Semana 8 (`EquipoInstaladoSerializer`):
`id`, `numero_serie`, `fecha_instalacion`, `fin_garantia`, `estado` (`OPERATIVO`, `MANTENIMIENTO` o `INACTIVO`), `producto`, `producto_nombre`, `cliente`, `cliente_razon_social`.

## Tabla de equivalencias
| Concepto trabajado en clase (cafetería) | Equivalente en el panel administrativo |
|---|---|
| `Practica` (padre con el estado) | **`PanelEquipos`**: padre que guarda el estado `equipos` y `busqueda` |
| `Catalogo` | **`ListadoEquipos`**: recibe los equipos (ya filtrados) y dibuja una fila por equipo |
| `ProductoCard` con botón Agregar | **`FilaEquipo`**: una fila con **dos botones de acción**: *Eliminar* y *Cambiar estado* (Operativo ↔ Mantenimiento), que avisan al padre con `onEliminar(id)` y `onCambiarEstado(id)` |
| `Carrito` (hermano del catálogo, con total) | **`ResumenEquipos`**: hermano del listado; muestra el total de equipos y el **conteo por estado** (operativos, en mantenimiento, inactivos), calculado con `filter()`/`reduce()` **sin `useState`** |
| `ProductoForm` con `onGuardar` | **`FormularioEquipo`**: formulario controlado de alta (serie, producto, cliente, fecha de instalación, estado) que entrega el equipo nuevo al padre con `onGuardar(equipo)` |
| `Buscador` con el estado en `App` | **`BuscadorEquipos`**: campo de texto controlado por el padre; filtra el listado por **`numero_serie`** |
| `Aviso` / título con `useEffect` | `useEffect` en `PanelEquipos` (o en el resumen): título de la pestaña `Equipos (N) — Panel` con dependencia `[equipos.length]`, y un aviso que desaparece a los 3 s con su limpieza |

## Reglas de la API (Semana 8) que usará el formulario de alta
Salen del modelo `EquipoInstalado` y de su serializer, que las aplica automáticamente al validar:
1. **`numero_serie` obligatorio y único** (`unique=True` en el modelo → en la API devuelve 400 si está vacío o ya existe).
2. **`estado` solo puede ser uno de los valores permitidos** (`OPERATIVO`, `MANTENIMIENTO`, `INACTIVO`) y `producto`, `cliente` y `fecha_instalacion` son obligatorios (campos sin `null/blank`).
3. Regla de coherencia propia del formulario: la garantía (`fin_garantia`) se calcula a partir de la fecha de instalación y la fecha no puede ser futura.

## Esquema del árbol de componentes
```
App
└── PanelEquipos            ESTADO: equipos (arreglo), busqueda (texto)
    ├── BuscadorEquipos       ↓ valor                          ↑ onCambiar(texto)
    ├── FormularioEquipo      ↓ equipos, productos, clientes   ↑ onGuardar(equipoNuevo)
    ├── ListadoEquipos        ↓ equipos (filtrados)            ↑ onEliminar(id), onCambiarEstado(id)
    │   └── FilaEquipo        ↓ equipo                         ↑ onEliminar(id), onCambiarEstado(id)
    └── ResumenEquipos        ↓ equipos   (hermano del listado; total y conteo por estado sin useState)
```
**↓ Props (datos que bajan):** `equipos`, `equipo`, `valor`, `productos`, `clientes`.
**↑ Funciones (avisos que suben):** `onCambiar`, `onGuardar`, `onEliminar`, `onCambiarEstado`.

Por qué el estado vive en `PanelEquipos`: lo necesitan a la vez el listado (para mostrarlo), el resumen (para calcular), el formulario (para agregar y comprobar series repetidas) y el buscador (para filtrar); `PanelEquipos` es su ancestro común más cercano.

## Ubicación de los archivos (checklist, puntos 1 y 2)
Los ejercicios de la Parte 1 siguen en `src/practica` y los componentes del panel irán cada uno en su archivo de `src/components` (`PanelEquipos.jsx`, `ListadoEquipos.jsx`, `FilaEquipo.jsx`, `FormularioEquipo.jsx`, `ResumenEquipos.jsx`, `BuscadorEquipos.jsx`), con los datos en `src/datosPanel.js`.

## Capturas
`captura_arbol_de_componentes.png`
