from rest_framework import serializers
from .models import Cliente

# serializers.py
from rest_framework import serializers
from .models import Cliente, Categoria, Proveedor, Producto, FichaTecnica, EquipoInstalado, TicketSoporte, Suministro


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre', 'descripcion']


class FichaTecnicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FichaTecnica
        fields = ['especificaciones', 'manual_usuario_url', 'norma_certificacion', 'fecha_revision']


class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = ['id', 'nombre_empresa', 'ruc_nit', 'contacto', 'telefono']


class ProductoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    # Permitir asignar la categoría mediante su ID al crear/actualizar
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), source='categoria', write_only=True, allow_null=True, required=False
    )
    
    ficha_tecnica = FichaTecnicaSerializer(read_only=True)

    class Meta:
        model = Producto
        fields = [
            'id', 'codigo_sku', 'nombre', 'marca', 'modelo', 
            'precio_base', 'meses_garantia', 'stock', 
            'categoria', 'categoria_id', 'ficha_tecnica'
        ]

    def validate_precio_base(self, value):
        if value < 0:
            raise serializers.ValidationError("El precio base no puede ser negativo.")
        return value


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'razon_social', 'numero_identificacion', 'email_contacto', 'telefono', 'direccion_fiscal', 'activo']

    # Ejercicio 10: validación propia -> validate_<campo>
    def validate_numero_identificacion(self, value):
        value = value.strip()
        if not value.isdigit():
            raise serializers.ValidationError("El RUC solo debe contener dígitos.")
        if len(value) != 11:
            raise serializers.ValidationError("El RUC debe tener exactamente 11 dígitos.")
        if not value.startswith(('10', '15', '17', '20')):
            raise serializers.ValidationError("El RUC debe iniciar con 10, 15, 17 o 20.")
        return value


class EquipoInstaladoSerializer(serializers.ModelSerializer):
    # Opcional: mostrar detalles del producto y cliente anidados
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')
    cliente_razon_social = serializers.ReadOnlyField(source='cliente.razon_social')

    class Meta:
        model = EquipoInstalado
        fields = [
            'id', 'numero_serie', 'fecha_instalacion', 'fin_garantia', 
            'estado', 'producto', 'producto_nombre', 'cliente', 'cliente_razon_social'
        ]


class TicketSoporteSerializer(serializers.ModelSerializer):
    # Mostramos información clave legible en lugar de solo IDs
    equipo_serie = serializers.ReadOnlyField(source='equipo.numero_serie')
    tecnico_nombre = serializers.ReadOnlyField(source='tecnico.nombre_completo')

    class Meta:
        model = TicketSoporte
        fields = [
            'id', 'codigo_ticket', 'descripcion_falla', 'prioridad', 
            'estado', 'fecha_creacion', 'equipo', 'equipo_serie', 
            'tecnico', 'tecnico_nombre'
        ]


# ---------------------------------------------------------------------------
# Ejercicio 7 - Recurso de solo lectura con relaciones anidadas
# Cliente (1) -> equipos instalados (N), cada equipo con el nombre de su producto.
# ---------------------------------------------------------------------------
class EquipoAnidadoSerializer(serializers.ModelSerializer):
    producto_nombre = serializers.ReadOnlyField(source='producto.nombre')  # toca la FK 'producto'

    class Meta:
        model = EquipoInstalado
        fields = ['id', 'numero_serie', 'estado', 'fecha_instalacion', 'fin_garantia', 'producto_nombre']


class ClienteConEquiposSerializer(serializers.ModelSerializer):
    equipos = EquipoAnidadoSerializer(many=True, read_only=True)  # relación inversa anidada

    class Meta:
        model = Cliente
        fields = ['id', 'razon_social', 'numero_identificacion', 'activo', 'equipos']
