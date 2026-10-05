from datetime import date
from decimal import Decimal

from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from django.db import transaction

from inventario.models import (
    Categoria, Cliente, EquipoInstalado, Producto, Proveedor, Suministro, TicketSoporte, Usuario,
)
from inventario.views import sumar_meses


# Relación 1:N -> una Categoría agrupa muchos Productos
CATEGORIAS = [
    ('Diagnóstico por Imagen', 'Equipos para obtención de imágenes médicas: ecógrafos, rayos X, etc.'),
    ('Monitoreo de Pacientes', 'Equipos para la vigilancia continua de signos vitales.'),
    ('Soporte Vital', 'Equipos críticos para mantener las funciones vitales del paciente.'),
]

# Entidad principal: Producto (sku, nombre, marca, modelo, precio_base, meses_garantia, stock, categoria)
PRODUCTOS = [
    ('ECO-MIN-DC70', 'Ecógrafo Doppler Color', 'Mindray', 'DC-70', '185000.00', 24, 8, 'Diagnóstico por Imagen'),
    ('RX-SIE-MOB3', 'Rayos X Portátil', 'Siemens', 'Mobilett Mira Max', '320000.00', 36, 2, 'Diagnóstico por Imagen'),
    ('MON-PHI-MX450', 'Monitor Multiparámetro', 'Philips', 'IntelliVue MX450', '42500.00', 24, 15, 'Monitoreo de Pacientes'),
    ('OXI-NON-7500', 'Pulsioxímetro de Mesa', 'Nonin', '7500', '3800.00', 12, 0, 'Monitoreo de Pacientes'),
    ('VEN-DRA-V500', 'Ventilador Mecánico', 'Dräger', 'Evita V500', '275000.00', 36, 3, 'Soporte Vital'),
    ('DES-ZOL-RS1', 'Desfibrilador Bifásico', 'ZOLL', 'R Series', '68000.00', 24, 5, 'Soporte Vital'),
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

# Clientes (numero_identificacion, razon_social, email_contacto, telefono, direccion_fiscal)
CLIENTES = [
    ('20100012345', 'Clínica San Gabriel S.A.', 'compras@sangabriel.pe', '014401122', 'Av. La Marina 1520, San Miguel, Lima'),
    ('20200067890', 'Hospital Regional de Arequipa', 'logistica@hrarequipa.gob.pe', '054382211', 'Av. Daniel Alcides Carrión 505, Arequipa'),
    ('20300054321', 'Centro Médico Santa Rosa E.I.R.L.', 'administracion@cmsantarosa.pe', '044255667', 'Jr. Pizarro 330, Trujillo'),
]

# Usuarios del sistema (email, nombre_completo, rol)
USUARIOS = [
    ('admin@inventario.pe', 'Patricia Rojas Vega', 'ADMIN'),
    ('jtorres@inventario.pe', 'Jorge Torres Lazo', 'TECNICO'),
    ('mhuaman@inventario.pe', 'María Huamán Ccori', 'TECNICO'),
]

# Equipos instalados históricos (numero_serie, sku, ruc cliente, fecha_instalacion, estado).
# Son instalaciones anteriores a la carga del stock actual, por eso no lo descuentan.
EQUIPOS = [
    ('MON-0101', 'MON-PHI-MX450', '20100012345', date(2024, 3, 12), 'OPERATIVO'),
    ('MON-0102', 'MON-PHI-MX450', '20100012345', date(2024, 3, 12), 'OPERATIVO'),
    ('MON-0103', 'MON-PHI-MX450', '20200067890', date(2025, 6, 20), 'MANTENIMIENTO'),
    ('MON-0104', 'MON-PHI-MX450', '20300054321', date(2023, 1, 18), 'INACTIVO'),
    ('VEN-0201', 'VEN-DRA-V500', '20200067890', date(2025, 2, 5), 'OPERATIVO'),
    ('VEN-0202', 'VEN-DRA-V500', '20200067890', date(2025, 2, 5), 'MANTENIMIENTO'),
    ('DES-0301', 'DES-ZOL-RS1', '20300054321', date(2024, 11, 3), 'OPERATIVO'),
    ('DES-0302', 'DES-ZOL-RS1', '20100012345', date(2023, 8, 27), 'MANTENIMIENTO'),
    ('OXI-0401', 'OXI-NON-7500', '20300054321', date(2022, 5, 9), 'INACTIVO'),
    ('RX-0501', 'RX-SIE-MOB3', '20200067890', date(2025, 9, 15), 'OPERATIVO'),
]

# Tickets de soporte (codigo, numero_serie del equipo, email del técnico, prioridad, estado, descripcion)
TICKETS = [
    ('TCK-0001', 'MON-0103', 'jtorres@inventario.pe', 'ALTA', 'EN_PROCESO', 'La alarma de SpO2 se activa sin motivo.'),
    ('TCK-0002', 'VEN-0202', 'mhuaman@inventario.pe', 'CRITICA', 'ABIERTO', 'El ventilador detiene el ciclo y marca error de presión.'),
    ('TCK-0003', 'DES-0302', 'jtorres@inventario.pe', 'MEDIA', 'ABIERTO', 'La batería no mantiene la carga más de 2 horas.'),
    ('TCK-0004', 'MON-0101', 'mhuaman@inventario.pe', 'BAJA', 'RESUELTO', 'Solicitud de recalibración de la pantalla táctil.'),
    ('TCK-0005', 'VEN-0201', None, 'ALTA', 'ABIERTO', 'Ruido anormal en la turbina durante la ventilación.'),
    ('TCK-0006', 'RX-0501', 'jtorres@inventario.pe', 'MEDIA', 'EN_PROCESO', 'Imágenes con artefactos en la parte inferior.'),
    ('TCK-0007', 'MON-0104', 'mhuaman@inventario.pe', 'BAJA', 'CERRADO', 'Equipo dado de baja tras evaluación técnica.'),
    ('TCK-0008', 'ECO-0001', 'jtorres@inventario.pe', 'MEDIA', 'ABIERTO', 'El transductor convexo no es reconocido.'),
]


class Command(BaseCommand):
    help = ('Registra datos de prueba: Categorías (1:N), Productos, Proveedores, Suministros (N:M through), '
            'Clientes, Usuarios, Equipos Instalados y Tickets de Soporte.')

    @transaction.atomic
    def handle(self, *args, **options):
        # update_or_create sobre campos únicos: el comando puede ejecutarse varias veces sin duplicar
        categorias = {}
        for nombre, descripcion in CATEGORIAS:
            categorias[nombre], _ = Categoria.objects.update_or_create(
                nombre=nombre, defaults={'descripcion': descripcion},
            )

        productos = {}
        for sku, nombre, marca, modelo, precio, garantia, stock, categoria in PRODUCTOS:
            datos = {
                'nombre': nombre, 'marca': marca, 'modelo': modelo,
                'precio_base': Decimal(precio), 'meses_garantia': garantia,
                'categoria': categorias[categoria],
            }
            # El stock solo se fija al crear: al volver a ejecutar no se pisan los movimientos ya registrados
            productos[sku], _ = Producto.objects.update_or_create(
                codigo_sku=sku, defaults=datos, create_defaults={**datos, 'stock': stock},
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

        clientes = {}
        for ruc, razon_social, email, telefono, direccion in CLIENTES:
            clientes[ruc], _ = Cliente.objects.update_or_create(
                numero_identificacion=ruc,
                defaults={'razon_social': razon_social, 'email_contacto': email,
                          'telefono': telefono, 'direccion_fiscal': direccion},
            )

        usuarios = {}
        for email, nombre, rol in USUARIOS:
            usuarios[email], _ = Usuario.objects.update_or_create(
                email=email, defaults={'nombre_completo': nombre, 'rol': rol},
                create_defaults={'nombre_completo': nombre, 'rol': rol, 'password_hash': make_password('Cambiar123')},
            )

        for serie, sku, ruc, fecha, estado in EQUIPOS:
            EquipoInstalado.objects.update_or_create(
                numero_serie=serie,
                defaults={
                    'producto': productos[sku], 'cliente': clientes[ruc], 'fecha_instalacion': fecha,
                    'fin_garantia': sumar_meses(fecha, productos[sku].meses_garantia), 'estado': estado,
                },
            )

        for codigo, serie, email_tecnico, prioridad, estado, descripcion in TICKETS:
            equipo = EquipoInstalado.objects.filter(numero_serie=serie).first()
            if equipo is None:
                # ECO-0001 proviene de una instalación registrada desde la aplicación
                continue
            TicketSoporte.objects.update_or_create(
                codigo_ticket=codigo,
                defaults={
                    'equipo': equipo, 'tecnico': usuarios.get(email_tecnico),
                    'prioridad': prioridad, 'estado': estado, 'descripcion_falla': descripcion,
                },
            )

        self.stdout.write(self.style.SUCCESS(
            f'Datos registrados: {Categoria.objects.count()} categorías, {Producto.objects.count()} productos, '
            f'{Proveedor.objects.count()} proveedores, {Suministro.objects.count()} suministros, '
            f'{Cliente.objects.count()} clientes, {Usuario.objects.count()} usuarios, '
            f'{EquipoInstalado.objects.count()} equipos, {TicketSoporte.objects.count()} tickets.'
        ))
