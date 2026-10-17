# Ejercicio 11 – ViewSets, router y códigos de estado

## Recursos expuestos con `ModelViewSet` + `DefaultRouter` bajo `/api/`
| Recurso | ViewSet | Ruta |
|---|---|---|
| Categoría | `CategoriaViewSet` (`views/productos.py`) | `/api/categorias/` |
| Cliente | `ClienteViewSet` (`views/clientes.py`) | `/api/clientes/` |

```python
router = DefaultRouter()
router.register(r'categorias', productos.CategoriaViewSet, basename='categoria')
router.register(r'clientes', clientes.ClienteViewSet, basename='cliente')
urlpatterns = [..., path('api/', include(router.urls))]
```

## Códigos de estado probados con `APITestCase` (`inventario/tests_api.py`, 11 tests, todos OK)

| Código | Situación | Petición (Cliente) | Resultado |
|---|---|---|---|
| **200 OK** | Listar / ver detalle / actualizar | `GET /api/clientes/` · `PATCH /api/clientes/<id>/` | Devuelve el/los clientes |
| **201 Created** | Crear con datos válidos | `POST /api/clientes/` | Devuelve el cliente creado con su `id` |
| **400 Bad Request** | Dato inválido (RUC `123`) | `POST /api/clientes/` | `{"numero_identificacion": ["El RUC debe tener exactamente 11 dígitos."]}` |
| **404 Not Found** | Id inexistente | `GET /api/clientes/9999/` | `{"detail": "No Cliente matches the given query."}` |
| **204 No Content** | Eliminar | `DELETE /api/clientes/<id>/` | Sin cuerpo; el registro deja de existir |

Los mismos 5 códigos se prueban también sobre `/api/categorias/` (400 con `nombre` vacío).

## Capturas
- `captura_tests_11_casos_ok.png`: salida de `python manage.py test inventario.tests_api -v 2`.
- `captura_peticiones_clientes.png`: peticiones y respuestas reales sobre `/api/clientes/` (`peticiones_clientes.txt` es el texto).

Los tests y las peticiones usan una base de datos de prueba temporal: `db.sqlite3` no se modifica.
