# Laboratorio 10 – Ejercicio 12: Relación anidada y formulario en la investigación propia

## Relación anidada (modelo intermedio)
`ProveedorCard` muestra, dentro de cada proveedor, un `SuministroItem` por cada suministro (modelo intermedio de la relación ManyToMany Producto ↔ Proveedor): un componente dentro de otro, con `key={s.id}` en el `map()` interno (ver Ej. 10). Un proveedor sin suministros muestra «Sin suministros registrados».

## Formulario controlado – `ListaProveedores`
- `proveedores` pasa a ser **estado** (`useState(iniciales)`) y el formulario guarda sus campos en un objeto de estado (`nombre_empresa`, `ruc_nit`, `contacto`, `telefono`); cada `<input>` es controlado (`value` + `onChange={manejarCambio}`, con un solo manejador que usa `name`).
- `onSubmit={manejarSubmit}` con `e.preventDefault()` para que el navegador no recargue la página.
- **Validación** (el RUC repite la regla de `validate_numero_identificacion` de la Semana 8): nombre obligatorio, RUC solo dígitos, exactamente 11, inicia con 10, 15, 17 o 20, no repetido en la lista (`ruc_nit` es `unique` en el modelo) y teléfono obligatorio. Si falla, se muestra el mensaje y no se agrega nada ni se borran los campos.
- Si es válido: `setProveedores([...proveedores, nuevo])` crea un **arreglo nuevo** (sin `push`), el proveedor nace con `suministros: []`, se limpian los campos y se quita el error. El contacto es opcional: vacío → valor por defecto «Sin contacto».

## Pruebas en el navegador
| Prueba | Datos | Resultado |
|---|---|---|
| Inválido: RUC con letras | `2051234ABCD` | «El RUC solo debe contener dígitos»; sigue habiendo 4 proveedores |
| Inválido: RUC corto | `2061122` | «El RUC debe tener exactamente 11 dígitos» |
| Inválido: prefijo | `30611223344` | «El RUC debe iniciar con 10, 15, 17 o 20» |
| Inválido: RUC duplicado | `20512345671` | «Ya existe un proveedor con ese RUC» |
| Inválido: sin nombre | nombre vacío | «El nombre de la empresa es obligatorio» |
| **Válido** | Servicios Médicos del Norte S.A.C., `20611223344`, teléfono `044123456`, sin contacto | 5 proveedores; campos limpios; sin error; **sin recargar la página**; la tarjeta nueva dice «Contacto: Sin contacto» y «Sin suministros registrados» |
| Buscar `norte` | — | Encuentra el proveedor recién agregado (el buscador del Ej. 11 usa la lista en estado) |

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola sin errores ni warnings.
- Como en el Ej. 8, el proveedor nuevo solo vive en el navegador: al recargar desaparece; guardarlo de verdad requerirá el `POST` a la API de Django (Semana 12).

## Capturas
- Código: `captura_codigo_ListaProveedores.jsx.png`
- `captura_01_antes.png`, `captura_02_envio_invalido_RUC_corto.png`, `captura_03_envio_invalido_RUC_duplicado.png`, `captura_04_envio_valido.png`
