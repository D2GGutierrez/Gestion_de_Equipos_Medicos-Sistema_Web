# Laboratorio 11 – Ejercicio 12: Formulario de alta que avisa al padre

## Qué se hizo
**`FormularioEquipo.jsx`** (hijo, nuevo) es un formulario con **campos controlados** (`value` + `onChange` con un solo manejador por `name`): número de serie, producto (`<select>`), cliente (`<select>`), fecha de instalación y estado. Valida antes de enviar y, si todo es correcto, **no agrega nada a la lista**: llama a `onGuardar(equipo)` con el registro (con la forma de la API: `numero_serie`, `fecha_instalacion`, `fin_garantia`, `estado`, `producto`, `producto_nombre`, `cliente`, `cliente_razon_social`) y deja los campos vacíos. La `fin_garantia` se calcula sumando los meses de garantía del producto a la fecha de instalación.

**`PanelEquipos.jsx`** (padre) define `guardarEquipo(nuevo)`: le asigna un `id` y agrega el equipo con un **arreglo nuevo**: `setEquipos([...equipos, { id, ...nuevo }])` (nunca `push`). Pasa al formulario `equipos` (para comprobar series repetidas), `productos`, `clientes` y `onGuardar`. Las listas de productos y clientes de los `<select>` están en `datosPanel.js`.

## Validación (reglas del modelo `EquipoInstalado` / API de la Semana 8)
1. `numero_serie` **obligatorio**.
2. `numero_serie` **único** (en el modelo es `unique=True`; se compara sin distinguir mayúsculas).
3. Producto y cliente seleccionados (campos obligatorios de la FK).
4. `fecha_instalacion` obligatoria y **no futura**.
Cada regla incumplida muestra su mensaje de error en rojo y no agrega nada ni borra los campos.

## Pruebas en el navegador
| Prueba | Datos | Resultado |
|---|---|---|
| **Inválida** – serie vacía | (vacío) | «El número de serie es obligatorio»; siguen 14 equipos |
| **Inválida** – serie repetida | `eco-0001` | «Ya existe un equipo con ese número de serie»; siguen 14 |
| **Inválida** – sin producto | `RX-0502` sin elegir producto | «Seleccione un producto»; siguen 14 |
| **Inválida** – fecha futura | `2030-01-01` | «La fecha de instalación no puede ser futura»; siguen 14. Los campos se conservan |
| **Válida** | `rx-0502`, Rayos X Portátil, Hospital Regional de Arequipa, 2026-11-10, Operativo | 15 equipos (`Equipos instalados (15)`); fila nueva `RX-0502` con garantía hasta **2029-11-10** (36 meses); **campos vacíos** y sin error |

La fila nueva forma parte del mismo estado del padre: sus botones funcionan (se cambió su estado a `MANTENIMIENTO` en la prueba).

## Verificación
- `npm run lint`: sin advertencias ni errores (código 0). `npm run build`: compila (código 0). Consola del navegador sin errores ni warnings.
- Sin `push` ni `splice` en los componentes del panel (`captura_sin_push_ni_splice.png`).
- El equipo agregado solo vive en el navegador: al recargar desaparece (guardarlo en Django es la Semana 12).

## Capturas
`captura_codigo_FormularioEquipo_validacion.png`, `captura_codigo_FormularioEquipo_campos.png`, `captura_codigo_PanelEquipos.jsx.png`, `captura_sin_push_ni_splice.png`, `captura_01_antes.png`, `captura_02_envio_invalido_serie_repetida.png`, `captura_03_alta_valida.png`
