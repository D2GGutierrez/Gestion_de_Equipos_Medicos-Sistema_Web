# Laboratorio 12 — Ejercicio 7: DELETE y PATCH

## Código (`src/practica/ListaPractica.jsx`)

```jsx
// DELETE: se quita del estado SOLO cuando el servidor confirma con 204
async function eliminar(id) {
  setFallo('')
  try {
    await api.delete(`/clientes/${id}/`)                        // 204 No Content
    setClientes(clientes.filter((c) => c.id !== id))            // arreglo NUEVO sin el cliente
  } catch {
    setFallo('No se pudo eliminar el cliente')
  }
}

// PATCH: envía solo el campo que cambia; el estado se actualiza con map()
async function cambiarActivo(cliente) {
  setFallo('')
  try {
    const respuesta = await api.patch(`/clientes/${cliente.id}/`, { activo: !cliente.activo }) // 200
    setClientes(clientes.map((c) => (c.id === cliente.id ? respuesta.data : c)))
  } catch {
    setFallo('No se pudo modificar el cliente')
  }
}
```

Cada fila tiene dos botones: **Activar/Desactivar** (PATCH) y **Eliminar** (DELETE).

## Resultados (probados en el navegador)

Para no tocar los clientes reales, se creó un cliente de prueba («Clínica Nueva Esperanza S.A.C.», POST 201), se modificó y se eliminó.

| Acción | Network | Pantalla |
|---|---|---|
| Desactivar | **PATCH** `/api/clientes/7/` con `{"activo": false}` → **200 OK** | La fila cambia de «(activo)» a «(inactivo)» y el botón pasa a «Activar» |
| Eliminar | **DELETE** `/api/clientes/7/` → **204 No Content** | La fila desaparece (de 4 a 3 clientes) |

Al terminar, la base volvió a tener los 3 clientes originales. La consola quedó sin errores ni advertencias, y `npm run lint` y `npm run build` terminan con código 0.

## Notas

- **PATCH vs PUT:** PATCH envía solo el campo que cambia (`activo`); PUT exigiría reenviar todo el registro. Por eso se eligió PATCH para este botón.
- **¿Por qué esperar la respuesta antes de cambiar el estado?** Si el servidor rechaza la operación (error de red, 404, etc.), la pantalla no debe mostrar algo que en la base de datos no ocurrió; en ese caso aparece el mensaje de error y la lista queda igual.
- El PATCH reemplaza la fila con `respuesta.data`, o sea con el registro tal como quedó guardado.

## Capturas

- `01_antes_patch.png`, `02_despues_patch.png` — página antes y después del PATCH.
- `03_antes_delete.png`, `04_despues_delete.png` — página antes y después del DELETE.
- `05_codigo_delete_patch.png`, `06_codigo_botones.png` — código.
- `07_network_patch_200.png`, `08_network_delete_204.png` — pestaña Network (método y código).
