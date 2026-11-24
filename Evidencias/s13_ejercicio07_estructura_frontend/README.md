# Laboratorio 13 — Ejercicio 7: Estructura base del frontend React

## 1. Qué se hizo

En `frontend/src`:

- **`components/`** ya existía de los laboratorios anteriores. Ya contiene `ProductoCard.jsx` (tarjeta de un producto con props y estado), así que **se reutiliza tal cual** en lugar de reemplazarla por un archivo vacío: vaciarla rompería `ListaProductos.jsx`, que la usa.
- **`pages/`** es nueva, con `ProductosPage.jsx` vacío (la pantalla del catálogo, que se llena en la Semana 14).
- **`api.js`** ya existía con la instancia de Axios; solo se ajustó la `baseURL` a la que pide el laboratorio.

```
frontend/src
├── api.js                      # instancia de Axios (baseURL de la API)
├── App.jsx
├── main.jsx
├── components/                 # piezas reutilizables
│   ├── ProductoCard.jsx        # ya existía: tarjeta de un producto
│   └── … (resto de componentes de los labs anteriores)
└── pages/                      # NUEVA: una pantalla por ruta
    └── ProductosPage.jsx       # NUEVO, vacío (se llena en la Semana 14)
```

## 2. `api.js`

```js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/', // dirección base de la API de Django
  timeout: 5000,
  headers: { 'Content-Type': 'application/json' },
})

export default api
```

Cambio respecto a antes: `baseURL` pasó de `http://127.0.0.1:8000/api` a `http://localhost:8000/api/`. Axios une la base con la ruta quitando la barra duplicada, así que las llamadas existentes siguen funcionando: `api.get('/clientes/')` → `http://localhost:8000/api/clientes/` y `api.get('equipos/', { params: { search: 'x' } })` → `http://localhost:8000/api/equipos/?search=x` (comprobado con `api.getUri`). CORS no cambia, porque depende del origen de React (`localhost:5173`), no del de la API.

## 3. Verificación

`npm run lint` sin advertencias y `npm run build` correcto (102 módulos). `ProductosPage.jsx` está vacío y nadie lo importa todavía, por eso no afecta al build.

## 4. Diferencia entre `components`, `pages` y `api.js`

- **`components/`**: piezas pequeñas y reutilizables (una tarjeta de producto, un botón, un formulario). Reciben datos por props y no saben en qué ruta están. Se pueden usar en varias pantallas.
- **`pages/`**: una pantalla completa asociada a una ruta (`/productos`, `/carrito`). Junta varios componentes, pide los datos y decide cómo se ve la pantalla. Una página usa componentes; un componente no usa páginas.
- **`api.js`**: el único lugar donde se configura la comunicación con Django (URL base, tiempo máximo, cabeceras). Los componentes y páginas lo importan y solo escriben el final de la ruta. Si la API cambia de puerto o de servidor, se modifica una sola línea.

Separarlos evita mezclar dibujo, datos y configuración en el mismo archivo.

## Capturas

- `01_estructura_frontend.png` — árbol de `frontend/src` con las carpetas y archivos del ejercicio.
- `02_api_js.png` — `api.js` con la nueva `baseURL`.
- `03_lint_build.png` — `npm run lint` y `npm run build`.
