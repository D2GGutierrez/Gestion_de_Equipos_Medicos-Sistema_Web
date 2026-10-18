# Estilos y verificación del flujo completo

## 1. Estilos
**Con `className` + `src/App.css`** (se importa con `import './App.css'`), 8 reglas: `.app`, `.titulo`, `.tarjeta`, `.agotado`, `.ultimas`, `.vacio`, `.lista`, `.equipos`.
```jsx
<div className="app">
  <h1 className="titulo">Gestión de Equipos Médicos</h1>
  <li key={p.id} className="tarjeta"> ... <span className="agotado">Agotado</span> ... <em className="ultimas">¡Últimas unidades!</em>
```
Se usa `className` (no `class`) porque `class` es palabra reservada de JavaScript.

**Con `style={{ }}`** (estilo en línea) en el total de cada cliente:
```jsx
<p style={{ fontWeight: 'bold', color: '#065f46' }}>Total de equipos: S/ {totalCliente(c).toFixed(2)}</p>
```
Las llaves externas son la expresión de JSX; las internas, el objeto de JavaScript (propiedades en camelCase: `fontWeight`).

## 2. Cambio de un dato y actualización del navegador
Con `npm run dev` y la página abierta, sin recargar, se cambió en el arreglo `productos` el stock del Desfibrilador de `0` a `2`:

| | Texto en pantalla |
|---|---|
| Antes | `Desfibrilador Bifásico — ... S/ 9800.75 · Agotado` (en rojo) |
| Después | `Desfibrilador Bifásico — ... S/ 9800.75 · Stock: 2 ¡Últimas unidades!` |

El navegador se actualizó solo (HMR de Vite): se verificó que seguía siendo la misma carga de página. Capturas: `captura_estilos_antes.png` y `captura_estilos_despues_cambio_dato.png`. Después de la prueba el dato se restauró a `0`.

## 3. `npm run lint` y `npm run build`
- `npm run lint` (oxlint): sin avisos ni errores, código de salida 0 (`captura_npm_run_lint.png`).
- `npm run build`:
```
vite v8.3.4 building client environment for production...
✓ 17 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.29 kB
dist/assets/index-B9mHoLUZ.css    0.45 kB │ gzip:  0.28 kB
dist/assets/index-DqSBz0k1.js   222.71 kB │ gzip: 69.73 kB
✓ built in 183ms
```
Genera la carpeta `dist/` (HTML, CSS y JS ya empaquetados y minificados) lista para publicar (`captura_npm_run_build.png`).

## 4. Diferencia con los Templates de la Semana 6
- **Dónde se arma el HTML.** En los Templates de Django, el servidor ejecuta la vista, rellena el template con `{{ }}` y `{% for %}` y envía la página ya terminada. Aquí el servidor solo entrega un `index.html` casi vacío y un JavaScript; es React, en el navegador, quien construye la página.
- **Cómo se actualiza.** Con Templates, cada cambio o enlace pide al servidor una página nueva (recarga completa). Con React, cuando cambian los datos solo se redibuja la parte afectada, sin recargar.
- **Datos.** El template recibe el contexto de la vista (acceso directo a la base de datos). React no ve la base de datos: solo puede trabajar con datos en JSON.
- **Estructura.** Un template es un archivo HTML con trozos de lógica; en React la interfaz son funciones de JavaScript (componentes) que devuelven JSX, y los estilos se aplican con `className`.
- Equivalencias: `{{ x }}` ↔ `{x}`, `{% for %}` ↔ `map()`, `{% if %}` ↔ ternario o `&&`.

## 5. Qué falta para conectarla con la API de la Semana 8
1. **Pedir los datos con `fetch`.** Hoy los arreglos están escritos a mano. Hay que llamar a la API (por ejemplo `fetch('http://127.0.0.1:8000/api/clientes-equipos/')`) dentro de un `useEffect` y guardar la respuesta en un estado con `useState`, en lugar de usar el arreglo fijo.
2. **Estados de carga y de error.** Mostrar "Cargando..." mientras llega la respuesta y un mensaje si falla.
3. **CORS.** React corre en `localhost:5173` y Django en `127.0.0.1:8000`: son orígenes distintos y el navegador bloquea la respuesta. Hay que instalar `django-cors-headers` y permitir `http://localhost:5173` (o configurar un proxy en `vite.config.js`).
4. **Ajustes en la API.** Hoy el router solo expone `categorias`, `clientes`, `clientes-equipos` y `tickets-detalle`: falta un endpoint de productos para la primera lista. Además, los equipos de `/api/clientes-equipos/` no traen `precio_base`, así que habría que agregarlo al serializer para calcular el total por cliente.
5. **Servidores en paralelo.** Tener `python manage.py runserver` y `npm run dev` corriendo a la vez.
6. Los decimales ya llegan como texto desde DRF; el `Number(...).toFixed(2)` que se usó se mantiene.
