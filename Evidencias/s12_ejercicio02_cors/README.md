# Laboratorio 12 — Ejercicio 2: Configurar CORS en Django

## 1. El error antes de configurar CORS

Con React corriendo en `http://localhost:5173/` y Django en `http://127.0.0.1:8000/`, se ejecutó en la consola del navegador:

```js
fetch('http://127.0.0.1:8000/api/clientes/')
```

Resultado (sin CORS):

```
Access to fetch at 'http://127.0.0.1:8000/api/clientes/' from origin 'http://localhost:5173'
has been blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present on the requested resource.
GET http://127.0.0.1:8000/api/clientes/ net::ERR_FAILED
Uncaught (in promise) TypeError: Failed to fetch
```

## 2. Configuración en Django

```
pip install django-cors-headers     # versión instalada: 4.9.0
```

`requirements.txt` quedó con la línea nueva: `django-cors-headers==4.9.0`.

Cambios en `gestion/settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'rest_framework',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',   # arriba, antes de CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    # ...
]

CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
]
```

## 3. El mismo fetch después de configurar CORS

```
HTTP 200 OK
access-control-allow-origin: http://localhost:5173
```

El navegador recibió los 3 clientes (el primero, «Clínica San Gabriel S.A.») y la consola quedó sin errores.

## 4. Por qué ocurre el bloqueo

El navegador aplica la **política del mismo origen**: una página solo puede leer respuestas del mismo origen (protocolo + dominio + puerto). React (`localhost:5173`) y Django (`127.0.0.1:8000`) son orígenes distintos, así que el navegador no entrega la respuesta a la página a menos que el servidor lo autorice con la cabecera `Access-Control-Allow-Origin`. El bloqueo lo hace el **navegador**, no Django: la petición llega al servidor (aparece 200 en su terminal) pero el navegador descarta la respuesta. Con `django-cors-headers`, Django añade esa cabecera solo para los orígenes de `CORS_ALLOWED_ORIGINS`; cualquier otro sitio sigue bloqueado. El middleware va arriba para que la cabecera se agregue a todas las respuestas, incluidos los errores.

## Capturas

- `01_cors_error_antes.png` — error de CORS en la consola.
- `02_pip_requirements.png` — instalación y `requirements.txt` actualizado.
- `03_settings_py.png` — cambios en `settings.py`.
- `04_fetch_despues.png` — el mismo fetch funcionando.
