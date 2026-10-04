from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from inventario.models import Categoria, Producto, Proveedor, Suministro


# Relación 1:N -> una Categoría agrupa muchos Productos
CATEGORIAS = [
    ('Diagnóstico por Imagen', 'Equipos para obtención de imágenes médicas: ecógrafos, rayos X, etc.'),
    ('Monitoreo de Pacientes', 'Equipos para la vigilancia continua de signos vitales.'),
    ('Soporte Vital', 'Equipos críticos para mantener las funciones vitales del paciente.'),
]

# Entidad principal: Producto (sku, nombre, marca, modelo, precio_base, meses_garantia, categoria)
PRODUCTOS = [
    ('ECO-MIN-DC70', 'Ecógrafo Doppler Color', 'Mindray', 'DC-70', '185000.00', 24, 'Diagnóstico por Imagen'),
    ('RX-SIE-MOB3', 'Rayos X Portátil', 'Siemens', 'Mobilett Mira Max', '320000.00', 36, 'Diagnóstico por Imagen'),
    ('MON-PHI-MX450', 'Monitor Multiparámetro', 'Philips', 'IntelliVue MX450', '42500.00', 24, 'Monitoreo de Pacientes'),
    ('OXI-NON-7500', 'Pulsioxímetro de Mesa', 'Nonin', '7500', '3800.00', 12, 'Monitoreo de Pacientes'),
    ('VEN-DRA-V500', 'Ventilador Mecánico', 'Dräger', 'Evita V500', '275000.00', 36, 'Soporte Vital'),
    ('DES-ZOL-RS1', 'Desfibrilador Bifásico', 'ZOLL', 'R Series', '68000.00', 24, 'Soporte Vital'),
]

# Proveedores (ruc_nit, nombre_empresa, contacto, telefono)
PROVEEDORES = [
    ('20512345671', 'MedTech Perú S.A.C.', 'Carla Mendoza', '014567890'),
    ('20498765432', 'BioEquipos Andinos S.R.L.', 'Luis Paredes', '012345678'),
    ('20600112233', 'Distribuidora Hospitalaria del Sur', 'Rosa Quispe', '054223344'),
    ('20555667788', 'Global Health Supply E.I.R.L.', 'Martín Salazar', '017788990'),
]

# Modelo intermedio N:M (sku, ruc proveedor, precio_compra, dias_entrega_promedio, es_proveedor_principal)
# Cada producto tiene un único proveedor principal; los demás son alternativos.
SUMINISTROS = [
    ('ECO-MIN-DC70', '20512345671', '152000.00', 15, True),
    ('ECO-MIN-DC70', '20498765432', '158500.00', 30, False),
    ('RX-SIE-MOB3', '20555667788', '268000.00', 45, True),
    ('RX-SIE-MOB3', '20512345671', '274900.00', 60, False),
    ('MON-PHI-MX450', '20498765432', '34800.00', 10, True),
    ('MON-PHI-MX450', '20600112233', '36200.00', 7, False),
    ('MON-PHI-MX450', '20555667788', '35500.00', 20, False),
    ('OXI-NON-7500', '20600112233', '2650.00', 3, True),
    ('VEN-DRA-V500', '20555667788', '229000.00', 40, True),
    ('VEN-DRA-V500', '20498765432', '236000.00', 25, False),
    ('DES-ZOL-RS1', '20512345671', '55200.00', 12, True),
    ('DES-ZOL-RS1', '20600112233', '57800.00', 5, False),
]


class Command(BaseCommand):
    help = 'Registra datos de prueba: Categorías (1:N), Productos, Proveedores y Suministros (N:M through).'

    @transaction.atomic
    def handle(self, *args, **options):
        # update_or_create sobre campos únicos: el comando puede ejecutarse varias veces sin duplicar
        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            categorias[nombre], _ = Categoria.objects.update_or_create(
                nombre=nombre, defaults={'descripcion': descripcion},
            )

        productos = {}
        for sku, nombre, marca, modelo, precio, garantia, categoria in PRODUCTOS:
            productos[sku], _ = Producto.objects.update_or_create(
                codigo_sku=sku,
                defaults={
                    'nombre': nombre, 'marca': marca, 'modelo': modelo,
                    'precio_base': Decimal(precio), 'meses_garantia': garantia,
                    'categoria': categorias[categoria],
                },
            )

        proveedores = {}
        for ruc, empresa, contacto, telefono in PROVEEDORES:
            proveedores[ruc], _ = Proveedor.objects.update_or_create(
                ruc_nit=ruc,
                defaults={'nombre_empresa': empresa, 'contacto': contacto, 'telefono': telefono},
            )

        for sku, ruc, precio, dias, principal in SUMINISTROS:
            Suministro.objects.update_or_create(
                producto=productos[sku], proveedor=proveedores[ruc],
                defaults={
                    'precio_compra': Decimal(precio), 'dias_entrega_promedio': dias,
                    'es_proveedor_principal': principal,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f'Datos registrados: {Categoria.objects.count()} categorías, {Producto.objects.count()} productos, '
            f'{Proveedor.objects.count()} proveedores, {Suministro.objects.count()} suministros.'
        ))
