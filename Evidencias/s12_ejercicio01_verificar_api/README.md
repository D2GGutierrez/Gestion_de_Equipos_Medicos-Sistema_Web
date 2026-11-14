# Laboratorio 12 — Ejercicio 1: Verificar la API y reconocer la petición

**Recurso simple elegido:** `Cliente` (el mismo que se usó en la Semana 8 para probar el CRUD y la validación `validate_numero_identificacion`).

## Petición documentada

| Dato | Valor |
|---|---|
| URL | `http://127.0.0.1:8000/api/clientes/` |
| Método HTTP | GET |
| Código de estado | 200 OK |
| Content-Type | `application/json` |

Fragmento del JSON recibido:

```json
[
  {
    "id": 1,
    "razon_social": "Clínica San Gabriel S.A.",
    "numero_identificacion": "20100012345",
    "email_contacto": "compras@sangabriel.pe",
    "telefono": "014401122",
    "direccion_fiscal": "Av. La Marina 1520, San Miguel, Lima",
    "activo": true
  }
]
```

## Operaciones CRUD del recurso

| Operación | Método HTTP | URL | Código esperado | Código obtenido |
|---|---|---|---|---|
| Listar | GET | `/api/clientes/` | 200 | 200 |
| Detalle | GET | `/api/clientes/1/` | 200 | 200 |
| Crear | POST | `/api/clientes/` | 201 | 201 |
| Crear con RUC inválido | POST | `/api/clientes/` | 400 | 400 — `{"numero_identificacion":["El RUC debe tener exactamente 11 dígitos."]}` |
| Modificar parcial | PATCH | `/api/clientes/4/` | 200 | 200 |
| Eliminar | DELETE | `/api/clientes/4/` | 204 | 204 |
| Detalle de un id borrado | GET | `/api/clientes/4/` | 404 | 404 — `{"detail":"No Cliente matches the given query."}` |

(El cliente creado en la prueba con `curl` se eliminó al final; la base quedó igual que al inicio.)

## Diferencia con un Template de Django

Un Template responde con una página HTML completa (cabecera, menú, estilos y los datos ya mezclados en el diseño) y, cuando cambia algo, el navegador recarga toda la página. La API REST responde solo con los datos en JSON y un código de estado: no trae diseño. Quien decide cómo dibujarlos es el cliente (en este proyecto, React), que puede pedirlos y actualizar solo la parte de la pantalla que cambió, sin recargar. Además, el código de estado (201, 204, 400, 404) le dice al cliente qué pasó con su petición.

## Capturas

- `01_navegador_api_clientes.png` — URL abierta en el navegador (GET, 200 OK, JSON).
- `02_navegador_json.png` — el mismo recurso en JSON puro (`?format=json`).
- `03_template_clientes.png` — para comparar: la vista con Template (`/clientes/`) devuelve HTML.
- `04_terminal_crud_curl.png` — pruebas de las operaciones CRUD con `curl` y sus códigos.
- `05_terminal_django.png` — terminal de `runserver` con las peticiones y sus códigos.
