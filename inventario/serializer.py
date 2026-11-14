import re
from rest_framework import serializers
from .models import Cliente

# serializers.py
from rest_framework import serializers
from .models import Cliente, Categoria, Proveedor, Producto, FichaTecnica, EquipoInstalado, TicketSoporte, Suministro, Usuario


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

    # Lab 12 Ej 9: regla de validación propia -> validate_<campo> (la usará el error 400 del panel)
    def validate_numero_serie(self, value):
        value = value.strip().upper()
        if not re.fullmatch(r'[A-Z]{2,4}-\d{4}', value):
            raise serializers.ValidationError("El número de serie debe tener el formato AAA-0000 (2 a 4 letras, guion y 4 dígitos).")
        duplicados = EquipoInstalado.objects.filter(numero_serie=value)
        if self.instance:
            duplicados = duplicados.exclude(pk=self.instance.pk)
        if duplicados.exists():
            raise serializers.ValidationError("Ya existe un equipo con ese número de serie.")
        return value

    # Validación entre campos: la garantía no puede terminar antes de la instalación
    def validate(self, datos):
        instalacion = datos.get('fecha_instalacion', getattr(self.instance, 'fecha_instalacion', None))
        garantia = datos.get('fin_garantia', getattr(self.instance, 'fin_garantia', None))
        if instalacion and garantia and garantia < instalacion:
            raise serializers.ValidationError({'fin_garantia': 'El fin de garantía no puede ser anterior a la fecha de instalación.'})
        return datos


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



# ---------------------------------------------------------------------------
# Ejercicio 12 - Ticket de solo lectura con relaciones anidadas (equipo -> cliente/producto, tecnico)
# ---------------------------------------------------------------------------
class TecnicoMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'nombre_completo', 'rol']


class EquipoMiniSerializer(serializers.ModelSerializer):
    cliente = serializers.ReadOnlyField(source='cliente.razon_social')  
    producto = serializers.ReadOnlyField(source='producto.nombre')       

    class Meta:
        model = EquipoInstalado
        fields = ['id', 'numero_serie', 'estado', 'cliente', 'producto']


class TicketDetalleSerializer(serializers.ModelSerializer):
    equipo = EquipoMiniSerializer(read_only=True)
    tecnico = TecnicoMiniSerializer(read_only=True)

    class Meta:
        model = TicketSoporte
        fields = ['id', 'codigo_ticket', 'prioridad', 'estado', 'fecha_creacion', 'equipo', 'tecnico']