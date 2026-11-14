# Laboratorio 12 — Ejercicio 3: Instalar Axios y crear una instancia

## Instalación

En la carpeta `frontend`:

```
npm install axios
```

`package.json` quedó con la dependencia `"axios": "^1.21.1"` (y `package-lock.json` actualizado).

## src/api.js

```js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api', // dirección base de la API de Django
  timeout: 5000, // si el servidor no responde en 5 s, Axios cancela y lanza un error
  headers: { 'Content-Type': 'application/json' },
})

export default api
```

Prueba rápida desde el navegador: `api.get('/clientes/')` pidió `http://127.0.0.1:8000/api/clientes/` y recibió 200 con 3 clientes. `npm run lint` y `npm run build` terminan con código 0.

## Ventaja de centralizar la dirección del servidor

La dirección de la API se escribe una sola vez en `api.js`. Los componentes importan `api` y solo indican la ruta final (`api.get('/clientes/')`), así que si el servidor cambia (otro puerto, otro equipo o producción) se modifica una línea y no cada componente. También se evitan errores de tipeo al repetir URLs largas, y las opciones comunes (timeout, cabeceras y, más adelante, un token de autenticación) se configuran en un solo lugar y valen para todas las peticiones.

## Capturas

- `01_api_js.png` — código de `src/api.js`.
- `02_package_json.png` — `package.json` con axios.
- `03_npm_install.png` — instalación de axios.
- `04_prueba_api_lint_build.png` — prueba de la instancia, lint y build.
