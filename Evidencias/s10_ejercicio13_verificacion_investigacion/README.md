# Laboratorio 10 – Ejercicio 13: Verificar la interfaz de la investigación propia

## 1. Consola del navegador
Se abrió la app en modo desarrollo (donde React sí emite advertencias) y se recorrió **toda** la interfaz: clic en todos los botones, los dos buscadores (con y sin texto) y los dos formularios (envío vacío, inválido y válido). La consola solo muestra 3 mensajes informativos (`[vite] connecting...`, `[vite] connected.` y el aviso de React DevTools). **No hay warnings ni errores**: ni de `key` en las listas ni de campos con `value` sin `onChange` (todos los inputs son controlados y todos los `map()` llevan `key` con el `id`).
→ `captura_consola_sin_advertencias.png`

## 2. `npm run lint` y `npm run build`
| Comando | Resultado |
|---|---|
| `npm run lint` (oxlint) | Sin advertencias ni errores, código de salida 0 |
| `npm run build` (vite) | `✓ 27 modules transformed`, `✓ built in 168ms`, código de salida 0 |

→ `captura_lint_y_build.png`

## 3. `node_modules` y `dist` no están en el repositorio
- `git ls-files | grep -E "(^|/)(node_modules|dist)(/|$)" | wc -l` → **0** archivos rastreados.
- `git check-ignore -v frontend/node_modules frontend/dist` → ambas carpetas las ignora `frontend/.gitignore` (líneas 10 y 11).
- `git status --short frontend` → sin cambios pendientes.

→ `captura_repositorio_sin_node_modules_ni_dist.png`

## 4. Checklist de la Parte 2
| # | Criterio | Dónde se cumple |
|---|---|---|
| 1 | Al menos tres componentes, cada uno en su archivo en `src/components` con nombre en mayúscula | `ListaProveedores`, `ProveedorCard`, `SuministroItem` (Ej. 10) |
| 2 | Props desestructuradas y valor por defecto o `children` | `contacto = 'Sin contacto'`, `principal = false`; `Tarjeta` usa `children` (Ej. 10) |
| 3 | Lista con `map()` y `key` | `ListaProveedores` (Ej. 10) |
| 4 | Relación 1:N con un componente dentro de otro | `SuministroItem` dentro de `ProveedorCard` (Ej. 10 y 12) |
| 5 | `useState` y `onClick` que lo cambia | Botón de favorito en `ProveedorCard` (Ej. 11, capturas antes y después) |
| 6 | Campo controlado que filtra la lista | Buscador de `ListaProveedores` (Ej. 11, tres búsquedas) |
| 7 | Formulario controlado con `onSubmit` + `preventDefault`, sin mutar el arreglo, con validación y mensaje | Formulario de proveedores (Ej. 12, envío válido e inválidos) |
| 8 | Consola sin advertencias, `lint` y `build` sin errores | Este ejercicio |
| 9 | Explicación de props, estado y qué falta para Django | Párrafo siguiente |

## 5. Justificación (checklist 9)
Las **props** resuelven cómo se reutiliza un componente: `ProveedorCard` no sabe de qué empresa habla hasta que el padre le pasa `nombre`, `ruc` o `suministros`, así que el mismo componente dibuja los cuatro proveedores y las props son de solo lectura (el padre es el dueño de los datos). El **estado** (`useState`) resuelve lo que cambia con el tiempo y debe reflejarse en pantalla: si un proveedor es favorito, lo que el usuario escribió en el buscador o la lista de proveedores tras agregar uno nuevo; cuando se llama a su función `set...`, React vuelve a dibujar el componente, algo que una variable común no logra. Aun así, todo esto vive solo en la memoria del navegador y desaparece al recargar. Para **guardar en Django** faltaría enviar el formulario a la API con `fetch` (`POST /api/proveedores/`), habilitar CORS en el backend, reemplazar los datos escritos a mano por un `GET` a la API (Semana 12), repetir la validación en el servidor (los serializers ya la tienen) y manejar los errores 400 que devuelva.

## Nota sobre cómo se obtuvieron las salidas
El código de la carpeta `frontend/src` es idéntico en la nube y en tu PC (se comparó el MD5 de todos los archivos). `lint`, `build` y la prueba de consola se ejecutaron sobre esa copia; las comprobaciones de Git se ejecutaron en tu repositorio. Las capturas de terminal y de consola son imágenes con el texto real de esas salidas.
