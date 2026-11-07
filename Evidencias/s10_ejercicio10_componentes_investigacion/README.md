# Laboratorio 10 – Ejercicio 10: Componentes y props de la investigación propia

Relación elegida de la investigación (Admin, Semana 5): **Proveedor** con su **modelo intermedio Suministro** (relación ManyToMany Producto ↔ Proveedor). Los datos son los 4 proveedores y 12 suministros reales de `db.sqlite3`, escritos a mano en `src/datosInvestigacion.js` con la forma de la API (decimales como texto, suministros anidados dentro de cada proveedor).

## Componentes (cada uno en su archivo dentro de `src/components`)
| Componente | Rol | Props |
|---|---|---|
| `ListaProveedores` | Lista: recorre el arreglo con `map()` y `key={p.id}` | `proveedores` |
| `ProveedorCard` | Registro + relación: muestra el proveedor y, dentro, sus suministros | `nombre`, `ruc`, `contacto` (**por defecto `'Sin contacto'`**), `telefono`, `suministros` |
| `SuministroItem` | Una fila del modelo intermedio | `producto`, `precio`, `dias`, `principal` (**por defecto `false`**) |

Además se reutiliza `Tarjeta` (con `children`) como contenedor de la sección en `App.jsx`.

## Correspondencia API → props
| Campo de la API | Prop |
|---|---|
| `nombre_empresa` | `nombre` |
| `ruc_nit` | `ruc` |
| `producto_nombre` | `producto` |
| `precio_compra` | `precio` |
| `dias_entrega_promedio` | `dias` |
| `es_proveedor_principal` | `principal` |

## Comprobaciones
- 4 proveedores, 12 suministros y 6 marcados como proveedor principal (`principal && …`); cada `<li>` de `map()` lleva `key` con el `id`.
- Valor por defecto probado: al quitar temporalmente el contacto del primer proveedor se mostró «Contacto: Sin contacto» (`captura_valor_por_defecto.png`); luego se restauró el dato.
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola sin errores ni warnings.

## Capturas
- Código: `captura_codigo_ListaProveedores.jsx.png`, `captura_codigo_ProveedorCard.jsx.png`, `captura_codigo_SuministroItem.jsx.png`, `captura_codigo_datosInvestigacion.js.png`
- Navegador: `captura_pagina_investigacion.png`, `captura_valor_por_defecto.png`
