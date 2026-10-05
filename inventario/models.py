from django.db import models
from django.utils import timezone


class Cliente(models.Model):
    razon_social = models.CharField(max_length=150)
    numero_identificacion = models.CharField(max_length=20, unique=True)
    email_contacto = models.EmailField()
    telefono = models.CharField(max_length=20)
    direccion_fiscal = models.CharField(max_length=255)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.razon_social


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    nombre_empresa = models.CharField(max_length=150)
    ruc_nit = models.CharField(max_length=20, unique=True)
    contacto = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)

    def __str__(self):
        return self.nombre_empresa


# Reglas de negocio de Producto. Cada método devuelve un QuerySet, por eso se pueden encadenar:
#   Producto.objects.disponibles().stock_bajo().por_nombre()
class ProductoQuerySet(models.QuerySet):
    STOCK_MINIMO = 3  # Por debajo o igual a este valor se considera stock bajo (reposición)

    def disponibles(self):
        """Productos que se pueden instalar: tienen al menos una unidad en almacén."""
        return self.filter(stock__gt=0)

    def agotados(self):
        """Productos sin unidades en almacén."""
        return self.filter(stock=0)

    def stock_bajo(self, limite=STOCK_MINIMO):
        """Productos con pocas unidades: hay que pedir reposición al proveedor principal."""
        return self.filter(stock__gt=0, stock__lte=limite)

    def con_stock_para(self, cantidad):
        """Productos cuyo stock alcanza para atender la cantidad solicitada."""
        return self.filter(stock__gte=cantidad)

    def instalados_en_mes(self, fecha=None):
        """Productos con al menos un equipo instalado en el mes de 'fecha' (por defecto, el mes actual)."""
        fecha = fecha or timezone.localdate()
        return self.filter(
            equipos__fecha_instalacion__year=fecha.year,
            equipos__fecha_instalacion__month=fecha.month,
        ).distinct()

    def con_detalle(self):
        """Trae en la misma consulta la Categoría (1:N) y la Ficha Técnica (1:1) para los listados."""
        return self.select_related('categoria', 'ficha_tecnica')

    def con_conteos(self):
        """Anota cuántos equipos instalados y cuántos proveedores tiene cada producto."""
        return self.annotate(
            num_equipos=models.Count('equipos', distinct=True),
            num_proveedores=models.Count('proveedores', distinct=True),
        )

    def por_nombre(self):
        return self.order_by('nombre')


class Producto(models.Model):
    codigo_sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=50)
    precio_base = models.DecimalField(max_digits=10, decimal_places=2)
    meses_garantia = models.IntegerField()
    stock = models.PositiveIntegerField(default=0, help_text="Unidades disponibles en almacén")

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name='productos',
        null=True,
        blank=True
    )

    proveedores = models.ManyToManyField(
        Proveedor,
        through='Suministro',
        related_name='productos',
        blank=True
    )

    objects = ProductoQuerySet.as_manager()

    def __str__(self):
        return f"{self.nombre} - {self.modelo}"


class Usuario(models.Model):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('VENTAS', 'Asesor Comercial'),
        ('LOGISTICA', 'Jefe de Inventario'),
        ('TECNICO', 'Técnico de Soporte'),
    ]
    nombre_completo = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    rol = models.CharField(max_length=20, choices=ROLES)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre_completo} ({self.rol})"


class EquipoInstalado(models.Model):
    ESTADOS = [
        ('OPERATIVO', 'Operativo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('INACTIVO', 'Inactivo'),
    ]
    numero_serie = models.CharField(max_length=100, unique=True)
    fecha_instalacion = models.DateField()
    fin_garantia = models.DateField()
    estado = models.CharField(max_length=30, choices=ESTADOS, default='OPERATIVO')
    
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='equipos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='equipos')

    def __str__(self):
        return f"Serie: {self.numero_serie} - {self.cliente.razon_social}"


# Reglas de negocio del soporte postventa. Los métodos devuelven un QuerySet y se pueden encadenar:
#   TicketSoporte.objects.pendientes().urgentes().sin_tecnico()
class TicketSoporteQuerySet(models.QuerySet):
    ESTADOS_PENDIENTES = ['ABIERTO', 'EN_PROCESO']    # El cliente todavía espera una solución
    ESTADOS_ATENDIDOS = ['RESUELTO', 'CERRADO']
    PRIORIDADES_URGENTES = ['ALTA', 'CRITICA']        # Equipo médico detenido o con riesgo para el paciente

    # Las reglas también como Q, para usarlas en Count(filter=...) desde otros modelos.
    # 'prefijo' es la ruta hasta el ticket, p. ej. 'tickets_asignados__' desde Usuario.
    @classmethod
    def q_pendiente(cls, prefijo=''):
        return models.Q(**{f'{prefijo}estado__in': cls.ESTADOS_PENDIENTES})

    @classmethod
    def q_atendido(cls, prefijo=''):
        return models.Q(**{f'{prefijo}estado__in': cls.ESTADOS_ATENDIDOS})

    @classmethod
    def q_urgente(cls, prefijo=''):
        return models.Q(**{f'{prefijo}prioridad__in': cls.PRIORIDADES_URGENTES})

    def pendientes(self):
        """Tickets abiertos o en proceso."""
        return self.filter(self.q_pendiente())

    def atendidos(self):
        """Tickets resueltos o cerrados."""
        return self.filter(self.q_atendido())

    def urgentes(self):
        """Tickets de prioridad alta o crítica."""
        return self.filter(self.q_urgente())

    def sin_tecnico(self):
        """Tickets que nadie ha tomado todavía."""
        return self.filter(tecnico__isnull=True)

    def de_tecnico(self, tecnico):
        return self.filter(tecnico=tecnico)

    def creados_en_mes(self, fecha=None):
        """Tickets reportados en el mes de 'fecha' (por defecto, el mes actual)."""
        fecha = fecha or timezone.localdate()
        return self.filter(fecha_creacion__year=fecha.year, fecha_creacion__month=fecha.month)

    def con_detalle(self):
        """Trae equipo, cliente y técnico en el mismo SELECT (evita el N+1 en los listados)."""
        return self.select_related('equipo', 'equipo__cliente', 'tecnico')

    def recientes(self):
        return self.order_by('-fecha_creacion')


class TicketSoporte(models.Model):
    PRIORIDADES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]
    ESTADOS = [
        ('ABIERTO', 'Abierto'),
        ('EN_PROCESO', 'En Proceso'),
        ('RESUELTO', 'Resuelto'),
        ('CERRADO', 'Cerrado'),
    ]
    codigo_ticket = models.CharField(max_length=20, unique=True)
    descripcion_falla = models.TextField()
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='MEDIA')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='ABIERTO')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    equipo = models.ForeignKey(EquipoInstalado, on_delete=models.CASCADE, related_name='tickets')
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets_asignados')

    objects = TicketSoporteQuerySet.as_manager()

    def __str__(self):
        return f"{self.codigo_ticket} - {self.estado}"

    

class FichaTecnica(models.Model):
    producto = models.OneToOneField(Producto, on_delete=models.CASCADE, related_name='ficha_tecnica')
    especificaciones = models.TextField(help_text="Detalles técnicos, dimensiones, peso, consumo eléctrico, etc.")
    manual_usuario_url = models.URLField(max_length=255, blank=True, null=True, help_text="Enlace al manual o documentación digital")
    norma_certificacion = models.CharField(max_length=100, blank=True, null=True, help_text="Ejemplo: ISO 9001, CE, RoHS, etc.")
    fecha_revision = models.DateField(auto_now=True)

    def __str__(self):
        return f"Ficha Técnica - {self.producto.nombre}"



class Suministro(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)
    dias_entrega_promedio = models.IntegerField(help_text="Tiempo estimado de entrega en días")
    es_proveedor_principal = models.BooleanField(default=False)
    fecha_ultimo_pedido = models.DateField(auto_now=True)

    class Meta:
        # Evita duplicar el mismo proveedor para el mismo producto
        unique_together = ('producto', 'proveedor')

    def __str__(self):
        return f"{self.proveedor.nombre_empresa} -> {self.producto.nombre}"