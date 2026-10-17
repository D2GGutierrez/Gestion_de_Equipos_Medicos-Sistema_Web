# Ejercicio 10 – Serializers y validación

## ModelSerializers (`inventario/serializer.py`)
`ClienteSerializer`, `ProductoSerializer` (con `CategoriaSerializer` y `FichaTecnicaSerializer` anidados),
`EquipoInstaladoSerializer`, `TicketSoporteSerializer`, `ProveedorSerializer`, `CategoriaSerializer`.

## Validaciones propias
- `ClienteSerializer.validate_numero_identificacion`: el RUC debe ser solo dígitos, de 11 dígitos y empezar con 10, 15, 17 o 20.
- `ProductoSerializer.validate_precio_base`: no permite precios negativos.

## Prueba en el shell (`python manage.py shell`)
```python
from inventario.serializer import ClienteSerializer
base = dict(razon_social='Clínica Demo SAC', email_contacto='demo@clinica.pe',
            telefono='014000000', direccion_fiscal='Av. Lima 123')
s = ClienteSerializer(data={**base, 'numero_identificacion': '20512345678'}); s.is_valid(); s.errors
```

| Dato | `is_valid()` | `errors` |
|---|---|---|
| RUC `20512345678` | `True` | `{}` |
| RUC `2051234ABCD` | `False` | `{'numero_identificacion': ['El RUC solo debe contener dígitos.']}` |
| RUC `12345` | `False` | `{'numero_identificacion': ['El RUC debe tener exactamente 11 dígitos.']}` |
| RUC `30512345678` | `False` | `{'numero_identificacion': ['El RUC debe iniciar con 10, 15, 17 o 20.']}` |
| Producto `precio_base=-5` | `False` | `{'precio_base': ['El precio base no puede ser negativo.']}` |
