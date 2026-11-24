# Laboratorio 13 — Ejercicio 6: Crear las apps de Django de la cafetería

## 1. Comandos

```
python manage.py startapp catalogo
python manage.py startapp pedidos
```

Cada comando crea una carpeta con esta estructura (ver `01_startapp_estructura.png`):

```
catalogo/                 pedidos/
├── __init__.py           ├── __init__.py
├── admin.py              ├── admin.py
├── apps.py               ├── apps.py
├── models.py             ├── models.py
├── tests.py              ├── tests.py
├── views.py              ├── views.py
└── migrations/           └── migrations/
    └── __init__.py           └── __init__.py
```

- `catalogo` queda para los productos y categorías de la cafetería.
- `pedidos` queda para el pedido y su detalle.

## 2. Registro en `gestion/settings.py`

```python
INSTALLED_APPS = [
    # ...
    'inventario',
    'catalogo',  # Lab 13 Ej 6: productos y categorías de la cafetería
    'pedidos',   # Lab 13 Ej 6: pedidos y sus detalles
    'rest_framework',
    'corsheaders',
]
```

## 3. Verificación

```
python manage.py check
System check identified no issues (0 silenced).
```

(`02_settings_installed_apps.png` y `03_manage_check.png`.) Las apps aún no tienen modelos, así que no hay migraciones nuevas.

## 4. Diferencia entre proyecto y app

El **proyecto** (`gestion/`) es la configuración global: `settings.py` (base de datos, apps instaladas, CORS), `urls.py` principal y el arranque (`manage.py`, `wsgi`/`asgi`). Hay uno solo y no tiene lógica de negocio.

Una **app** (`inventario`, `catalogo`, `pedidos`) es un módulo con una responsabilidad concreta: sus propios modelos, vistas, serializers, URLs y pruebas. Un proyecto contiene varias apps, y cada una puede reutilizarse en otro proyecto. Django solo la reconoce cuando está en `INSTALLED_APPS`; por eso crear la carpeta no basta: sin registrarla, sus modelos no se migran ni aparecen en el admin.

Separar el catálogo de los pedidos evita un único módulo gigante: los productos y su stock cambian por razones distintas que los pedidos y sus estados, y cada equipo o semana puede trabajar uno sin tocar el otro.

## 5. Nota sobre el repositorio

El proyecto sigue siendo el mismo (`gestion`) y ya tiene la app `inventario` de equipos médicos. Las apps `catalogo` y `pedidos` se agregan al lado, sin tocar `inventario`. En la Parte 2 (proyecto integrador) se decidirá qué apps se reutilizan o se renombran para la gestión de equipos.

## Capturas

- `01_startapp_estructura.png` — comandos `startapp` y estructura creada.
- `02_settings_installed_apps.png` — `INSTALLED_APPS` con las dos apps.
- `03_manage_check.png` — `python manage.py check` sin errores.
