# Laboratorio 10 – Ejercicio 8: Formulario controlado con validación

## Qué se hizo
Todo en `ListaProductos` (el estado se maneja en el componente que lo usa; no se pasan funciones entre componentes):
- `productos` pasa a ser **estado** (`useState(iniciales)`, iniciado con lo que llega por props).
- `form` es un estado con los campos `nombre, marca, modelo, precio, stock`; cada `<input>` es **controlado** (`value` + `onChange={manejarCambio}`), con un solo manejador que usa el atributo `name`.
- `onSubmit={manejarSubmit}` en el `<form>`; dentro, `e.preventDefault()` evita la recarga de la página.
- **Validación** (reglas de la API de la Semana 8): nombre obligatorio, `precio > 0`, `stock` entero ≥ 0. Si falla, se muestra un mensaje (estado `error`) y **no** se agrega nada ni se borran los campos.
- Si es válido: `setProductos([...productos, nuevo])` crea un **nuevo arreglo** (nunca `productos.push`, porque mutar el arreglo no avisa a React), `setForm(FORM_VACIO)` limpia los campos y `setError('')` quita el mensaje.
- La marca es opcional: si se deja vacía se usa el valor por defecto `'Sin marca'` del Ejercicio 3.

## Pruebas en el navegador
| Prueba | Resultado |
|---|---|
| Estado inicial | 5 productos |
| Precio = 0 | «El precio debe ser mayor a 0»; sigue habiendo 5 y los campos se conservan |
| Nombre vacío | «El nombre es obligatorio»; sigue habiendo 5 |
| Datos válidos (Bomba de Infusión, B. Braun, Infusomat, 1250.50, stock 5) | 6 productos, campos limpios, sin mensaje de error y **sin recargar la página** |
| Producto sin marca (Cama Clínica, stock 0) | Aparece «Sin marca» y «Agotado» |
| Buscar `bomba` | Encuentra el producto recién agregado (el buscador del Ej. 7 trabaja sobre la lista en estado) |

## ¿Qué falta para guardar de verdad en Django?
Ahora el producto solo existe en la memoria del navegador: al recargar (F5) desaparece. Para guardarlo faltaría:
1. **Enviar los datos a la API** con `fetch`/`axios` (`POST /api/productos/`) en lugar de solo modificar el estado (Semana 12).
2. **CORS** en Django (`django-cors-headers`) para que el frontend (`localhost:5173`) pueda llamar al backend (`localhost:8000`).
3. **Categoría real**: la API pide `categoria` (id); aquí se usa «Sin categoría» provisional, haría falta un `<select>` cargado desde `/api/categorias/`.
4. **Validar también en el servidor** (los serializers de Django ya lo hacen): la validación del navegador es solo comodidad para el usuario y se puede saltar.
5. **Usar el `id` y los datos que responde Django** (el `id` lo asigna la base de datos; aquí se calcula uno provisional) y manejar los errores 400 de la API (por ejemplo mostrar lo que diga el serializer).

## Verificación
- `npm run lint`: sin errores (exit 0). `npm run build`: compila correctamente. Consola sin errores ni warnings.

## Capturas
- `captura_codigo_ListaProductos.jsx.png`
- `captura_01_antes.png`, `captura_02_error_precio.png`, `captura_03_producto_agregado.png`
