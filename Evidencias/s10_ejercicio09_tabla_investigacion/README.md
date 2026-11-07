# Laboratorio 10 – Ejercicio 9: Identificar los componentes de la investigación propia

Investigación propia (Admin, Semana 5): modelos de `inventario`. La interfaz de la Parte 2 se centra en **Proveedor** y su modelo intermedio **Suministro** (ManyToMany Producto ↔ Proveedor), más el registro **Cliente** para el formulario.

## Tabla de equivalencias
| Qué se necesita | Componente / elemento | Datos y detalle |
|---|---|---|
| Mostrar **un registro** | `ProveedorCard` | `nombre_empresa`, `ruc_nit`, `contacto`, `telefono` |
| Mostrar la **lista** | `ListaProveedores` | `map()` con `key = id` |
| Mostrar la **relación anidada** (modelo intermedio) | `SuministroItem` dentro de `ProveedorCard` | `producto_nombre`, `precio_compra`, `dias_entrega_promedio`, `es_proveedor_principal` |
| **Botón con estado** | Botón «Marcar como favorito» en `ProveedorCard` (`useState` booleano, `onClick`) | Cambia el texto y el estilo del botón |
| **Buscador controlado** | Campo en `ListaProveedores` | Filtra por `nombre_empresa` sin distinguir mayúsculas |
| **Formulario controlado** | Formulario «Agregar proveedor» en `ListaProveedores` (`onSubmit` + `preventDefault`) | Campos: `nombre_empresa`, `ruc_nit`, `contacto`, `telefono` |

## Regla de la API (Semana 8) que se usará para validar
`ProveedorSerializer` / `ClienteSerializer` del proyecto validan el RUC (`validate_numero_identificacion`): **solo dígitos, exactamente 11 y debe iniciar con 10, 15, 17 o 20**. El formulario de proveedor aplicará esa misma regla sobre `ruc_nit`, además de que el nombre de la empresa sea obligatorio. (El `ruc_nit` también es `unique=True` en el modelo; se validará que no se repita en la lista.)
