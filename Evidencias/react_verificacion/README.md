# Ejercicio 13 – Verificar la interfaz

## 1. Consola del navegador
Con `npm run dev` abierto en http://localhost:5173/ la consola solo muestra los mensajes informativos de Vite y de React DevTools: **0 advertencias y 0 errores** (8 tarjetas y 14 `<li>`, todos los de `map()` con `key`).
Prueba de control: al quitar a propósito `key={p.id}` de un `<li>`, la consola muestra `Each child in a list should have a unique "key" prop`; con la `key` puesta, desaparece. Así se comprueba que la revisión detecta el problema.
Captura: `captura_consola_sin_advertencias.png`.

## 2. `npm run lint` y `npm run build`
- `npm run lint` (oxlint): sin avisos ni errores, código de salida 0.
- `npm run build` (Vite 8.3.4): correcto, código de salida 0.
```
✓ 17 modules transformed.
dist/index.html                   0.45 kB │ gzip:  0.29 kB
dist/assets/index-B9mHoLUZ.css    0.45 kB │ gzip:  0.28 kB
dist/assets/index-DSgB0l2I.js   222.80 kB │ gzip: 69.75 kB
✓ built in 210ms
```
Captura: `captura_lint_y_build.png`.

## 3. `node_modules` y `dist` fuera del repositorio
En el repositorio (`.git` de la carpeta del proyecto):
- `git ls-files` no contiene ningún archivo de `node_modules/` ni de `dist/` (0 archivos rastreados). `frontend/` solo tiene su código fuente: `index.html`, `package.json`, `package-lock.json`, `vite.config.js`, `src/`, `public/`, etc.
- `frontend/.gitignore` (creado por Vite) los excluye: `node_modules` (línea 10) y `dist` (línea 11); `git check-ignore -v` lo confirma.
- Las carpetas tampoco existen físicamente en tu copia del proyecto (se crean con `npm install` y `npm run build`).
Captura: `captura_repositorio_sin_node_modules_ni_dist.png`.

Nota: el proyecto no tiene `.gitignore` en la raíz. Hoy el repositorio sí rastrea archivos `__pycache__/*.pyc` y `db.sqlite3`; conviene añadir un `.gitignore` raíz (`.venv/`, `__pycache__/`, `*.pyc`) si se quiere un repositorio más limpio.
Nota: lint, build y la prueba de consola se ejecutaron en el entorno Linux de la sesión; repite `npm run lint` y `npm run build` en tu PC si tu docente pide las capturas de tu terminal.
