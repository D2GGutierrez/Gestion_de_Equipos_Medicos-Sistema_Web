# Ejercicio 1 – Verificar el entorno: Node.js y npm

## Versiones obtenidas
```
$ node -v
v22.23.2
$ npm -v
10.9.8
```
Captura: `captura_node_npm_versiones.png`. Node.js 22 es una versión LTS, por lo que no hace falta instalar nada.

> Nota: estas versiones se obtuvieron en el entorno Linux de la sesión de Claude, no en la terminal de Windows del equipo.
> Para la entrega, ejecutar `node -v` y `npm -v` en tu propia terminal (PowerShell o CMD) y reemplazar la captura.
> Si no estuvieran instalados: descargar la versión **LTS** desde https://nodejs.org (incluye npm) y reiniciar la terminal.

## Equivalencias Python/Django ↔ Node.js/React

| Elemento | Python / Django | Node.js / React |
|---|---|---|
| Lenguaje | Python (archivos `.py`) | JavaScript (archivos `.js` / `.jsx`) |
| Entorno de ejecución | Intérprete de Python | Node.js (motor V8 fuera del navegador) |
| Gestor de paquetes | `pip` | `npm` |
| Archivo de dependencias | `requirements.txt` | `package.json` (y `package-lock.json` con las versiones exactas) |
| Carpeta de dependencias | entorno virtual (`venv/`, con `site-packages`) | `node_modules/` |
| Instalar dependencias | `pip install -r requirements.txt` | `npm install` |
| Levantar el servidor de desarrollo | `python manage.py runserver` | `npm run dev` (Vite) o `npm start` (Create React App) |

Diferencia de fondo: Django es un framework de backend completo (ORM, rutas, admin); React es solo una biblioteca para construir interfaces, que se ejecuta en el navegador y consume la API de Django.
