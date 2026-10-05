from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Count
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Categoria, Cliente, EquipoInstalado, Producto, Proveedor, Suministro, TicketSoporte, TicketSoporteQuerySet, Usuario,
)


class DatosBase(TestCase):
    """Datos mínimos compartidos por todos los tests (se crean en una BD de prueba aparte)."""

    @classmethod
    def setUpTestData(cls):
        cls.categoria = Categoria.objects.create(nombre='Monitoreo')
        cls.monitor = Producto.objects.create(
            codigo_sku='MON-1', nombre='Monitor', marca='Philips', modelo='MX450',
            precio_base=Decimal('1000.00'), meses_garantia=24, stock=10, categoria=cls.categoria,
        )
        cls.oximetro = Producto.objects.create(
            codigo_sku='OXI-1', nombre='Oxímetro', marca='Nonin', modelo='7500',
            precio_base=Decimal('100.00'), meses_garantia=12, stock=0, categoria=cls.categoria,
        )
        cls.ventilador = Producto.objects.create(
            codigo_sku='VEN-1', nombre='Ventilador', marca='Dräger', modelo='V500',
            precio_base=Decimal('5000.00'), meses_garantia=36, stock=2,
        )
        cls.proveedor = Proveedor.objects.create(
            nombre_empresa='MedTech', ruc_nit='20512345671', contacto='Carla', telefono='014567890',
        )
        cls.cliente = Cliente.objects.create(
            razon_social='Clínica San Gabriel', numero_identificacion='20100012345',
            email_contacto='compras@sangabriel.pe', telefono='014401122', direccion_fiscal='Av. La Marina 1520',
        )
        cls.tecnico = Usuario.objects.create(
            nombre_completo='Jorge Torres', email='jtorres@inventario.pe', password_hash='x', rol='TECNICO',
        )
        hoy = timezone.localdate()
        cls.equipo_mes = EquipoInstalado.objects.create(
            numero_serie='MON-0001', producto=cls.monitor, cliente=cls.cliente,
            fecha_instalacion=hoy, fin_garantia=hoy + timedelta(days=730),
        )
        cls.equipo_antiguo = EquipoInstalado.objects.create(
            numero_serie='VEN-0001', producto=cls.ventilador, cliente=cls.cliente,
            fecha_instalacion=date(2023, 1, 10), fin_garantia=date(2026, 1, 10),
        )
        cls.ticket = TicketSoporte.objects.create(
            codigo_ticket='TCK-1', descripcion_falla='Alarma falsa', equipo=cls.equipo_mes, tecnico=cls.tecnico,
        )


class ProductoQuerySetTests(DatosBase):

    def nombres(self, qs):
        return sorted(qs.values_list('nombre', flat=True))

    def test_disponibles_y_agotados(self):
        self.assertEqual(self.nombres(Producto.objects.disponibles()), ['Monitor', 'Ventilador'])
        self.assertEqual(self.nombres(Producto.objects.agotados()), ['Oxímetro'])

    def test_stock_bajo_excluye_agotados(self):
        self.assertEqual(self.nombres(Producto.objects.stock_bajo()), ['Ventilador'])
        self.assertEqual(self.nombres(Producto.objects.stock_bajo(limite=10)), ['Monitor', 'Ventilador'])

    def test_con_stock_para(self):
        self.assertEqual(self.nombres(Producto.objects.con_stock_para(3)), ['Monitor'])

    def test_instalados_en_mes(self):
        self.assertEqual(self.nombres(Producto.objects.instalados_en_mes()), ['Monitor'])
        self.assertEqual(self.nombres(Producto.objects.instalados_en_mes(date(2023, 1, 1))), ['Ventilador'])

    def test_metodos_encadenables(self):
        # Cada método devuelve un QuerySet, así que se pueden combinar entre sí y con filter()
        qs = Producto.objects.disponibles().instalados_en_mes().con_conteos().por_nombre()
        self.assertEqual([p.nombre for p in qs], ['Monitor'])
        self.assertEqual(qs[0].num_equipos, 1)
        self.assertEqual(list(Producto.objects.filter(categoria=self.categoria).disponibles()), [self.monitor])

    def test_por_nombre(self):
        self.assertEqual([p.nombre for p in Producto.objects.por_nombre()], ['Monitor', 'Oxímetro', 'Ventilador'])


class ViewsConQuerySetTests(DatosBase):

    def test_lista_productos_filtros(self):
        url = reverse('lista_productos')
        casos = {
            '': ['Monitor', 'Oxímetro', 'Ventilador'],
            '?stock=disponibles': ['Monitor', 'Ventilador'],
            '?stock=bajo': ['Ventilador'],
            '?stock=agotados': ['Oxímetro'],
            '?mes=actual': ['Monitor'],
            '?stock=bajo&mes=actual': [],
        }
        for query, esperado in casos.items():
            with self.subTest(query=query):
                r = self.client.get(url + query)
                self.assertEqual(r.status_code, 200)
                self.assertEqual([p.nombre for p in r.context['productos']], esperado)

    def test_reporte(self):
        r = self.client.get(reverse('reporte'))
        self.assertEqual(r.status_code, 200)
        self.assertEqual([p.nombre for p in r.context['stock_bajo']], ['Ventilador'])
        self.assertEqual([p.nombre for p in r.context['agotados']], ['Oxímetro'])
        self.assertEqual([p.nombre for p in r.context['instalados_mes']], ['Monitor'])

    def test_registrar_instalacion_descuenta_stock(self):
        r = self.client.post(reverse('registrar_instalacion'), {
            'producto': self.monitor.pk, 'cliente': self.cliente.pk,
            'fecha_instalacion': timezone.localdate().isoformat(), 'numeros_serie': 'MON-0100\nMON-0101',
        })
        self.assertRedirects(r, reverse('registrar_instalacion'))
        self.monitor.refresh_from_db()
        self.assertEqual(self.monitor.stock, 8)

    def test_registrar_instalacion_sin_stock_no_cambia_nada(self):
        equipos_antes = EquipoInstalado.objects.count()
        r = self.client.post(reverse('registrar_instalacion'), {
            'producto': self.ventilador.pk, 'cliente': self.cliente.pk,
            'fecha_instalacion': timezone.localdate().isoformat(), 'numeros_serie': 'V-1\nV-2\nV-3',
        })
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Stock insuficiente')
        self.assertEqual(EquipoInstalado.objects.count(), equipos_antes)
        self.ventilador.refresh_from_db()
        self.assertEqual(self.ventilador.stock, 2)


class CrudSemana3Tests(DatosBase):
    """El CRUD de la Semana 3 debe seguir funcionando con el manager personalizado."""

    def test_listados(self):
        for nombre in ['lista_productos', 'productos_proveedores', 'lista_clientes', 'lista_usuarios',
                       'lista_equipos', 'lista_tickets']:
            with self.subTest(vista=nombre):
                self.assertEqual(self.client.get(reverse(nombre)).status_code, 200)
        self.assertEqual(self.client.get(reverse('detalle_categoria', args=[self.categoria.pk])).status_code, 200)

    def test_crud_producto(self):
        # CREATE
        self.assertEqual(self.client.get(reverse('crear_producto')).status_code, 200)
        r = self.client.post(reverse('crear_producto'), {
            'codigo_sku': 'DES-1', 'nombre': 'Desfibrilador', 'marca': 'ZOLL', 'modelo': 'R Series',
            'precio_base': '6800.00', 'meses_garantia': 24, 'stock': 5, 'categoria': self.categoria.pk,
        })
        self.assertRedirects(r, reverse('lista_productos'))
        nuevo = Producto.objects.get(codigo_sku='DES-1')
        self.assertEqual(nuevo.stock, 5)

        # UPDATE
        r = self.client.post(reverse('editar_producto', args=[nuevo.pk]), {
            'codigo_sku': 'DES-1', 'nombre': 'Desfibrilador Bifásico', 'marca': 'ZOLL', 'modelo': 'R Series',
            'precio_base': '7000.00', 'meses_garantia': 24, 'stock': 4, 'categoria': self.categoria.pk,
        })
        self.assertRedirects(r, reverse('lista_productos'))
        nuevo.refresh_from_db()
        self.assertEqual((nuevo.nombre, nuevo.precio_base, nuevo.stock), ('Desfibrilador Bifásico', Decimal('7000.00'), 4))

        # DELETE (GET muestra la confirmación, POST elimina)
        self.assertEqual(self.client.get(reverse('eliminar_producto', args=[nuevo.pk])).status_code, 200)
        r = self.client.post(reverse('eliminar_producto', args=[nuevo.pk]))
        self.assertRedirects(r, reverse('lista_productos'))
        self.assertFalse(Producto.objects.filter(pk=nuevo.pk).exists())

    def test_crud_suministro(self):
        r = self.client.post(reverse('crear_suministro', args=[self.monitor.pk]), {
            'proveedor': self.proveedor.pk, 'precio_compra': '800.00',
            'dias_entrega_promedio': 10, 'es_proveedor_principal': 'on',
        })
        self.assertRedirects(r, reverse('productos_proveedores'))
        suministro = Suministro.objects.get(producto=self.monitor, proveedor=self.proveedor)

        r = self.client.post(reverse('editar_suministro', args=[suministro.pk]), {
            'proveedor': self.proveedor.pk, 'precio_compra': '750.00', 'dias_entrega_promedio': 7,
        })
        self.assertRedirects(r, reverse('productos_proveedores'))
        suministro.refresh_from_db()
        self.assertEqual((suministro.precio_compra, suministro.es_proveedor_principal), (Decimal('750.00'), False))

        r = self.client.post(reverse('eliminar_suministro', args=[suministro.pk]))
        self.assertRedirects(r, reverse('productos_proveedores'))
        self.assertFalse(Suministro.objects.filter(pk=suministro.pk).exists())

    def test_editar_y_eliminar_cliente(self):
        r = self.client.post(reverse('editar_cliente', args=[self.cliente.pk]), {
            'razon_social': 'Clínica San Gabriel S.A.', 'numero_identificacion': '20100012345',
            'email_contacto': 'compras@sangabriel.pe', 'telefono': '014401122',
            'direccion_fiscal': 'Av. La Marina 1520', 'activo': 'on',
        })
        self.assertRedirects(r, reverse('lista_clientes'))
        self.cliente.refresh_from_db()
        self.assertEqual(self.cliente.razon_social, 'Clínica San Gabriel S.A.')

        r = self.client.post(reverse('eliminar_cliente', args=[self.cliente.pk]))
        self.assertRedirects(r, reverse('lista_clientes'))
        self.assertFalse(Cliente.objects.exists())

    def test_editar_y_eliminar_usuario(self):
        r = self.client.post(reverse('editar_usuario', args=[self.tecnico.pk]), {
            'nombre_completo': 'Jorge Torres Lazo', 'email': 'jtorres@inventario.pe', 'rol': 'TECNICO', 'activo': 'on',
        })
        self.assertRedirects(r, reverse('lista_usuarios'))
        self.tecnico.refresh_from_db()
        self.assertEqual(self.tecnico.nombre_completo, 'Jorge Torres Lazo')

        r = self.client.post(reverse('eliminar_usuario', args=[self.tecnico.pk]))
        self.assertRedirects(r, reverse('lista_usuarios'))
        self.assertFalse(Usuario.objects.filter(pk=self.tecnico.pk).exists())

    def test_editar_y_eliminar_equipo(self):
        r = self.client.post(reverse('editar_equipo', args=[self.equipo_antiguo.pk]), {
            'numero_serie': 'VEN-0001', 'fecha_instalacion': '2023-01-10', 'fin_garantia': '2026-01-10',
            'estado': 'MANTENIMIENTO', 'producto': self.ventilador.pk, 'cliente': self.cliente.pk,
        })
        self.assertRedirects(r, reverse('lista_equipos'))
        self.equipo_antiguo.refresh_from_db()
        self.assertEqual(self.equipo_antiguo.estado, 'MANTENIMIENTO')

        r = self.client.post(reverse('eliminar_equipo', args=[self.equipo_antiguo.pk]))
        self.assertRedirects(r, reverse('lista_equipos'))
        self.assertFalse(EquipoInstalado.objects.filter(pk=self.equipo_antiguo.pk).exists())

    def test_editar_y_eliminar_ticket(self):
        r = self.client.post(reverse('editar_ticket', args=[self.ticket.pk]), {
            'codigo_ticket': 'TCK-1', 'descripcion_falla': 'Alarma falsa', 'prioridad': 'ALTA',
            'estado': 'EN_PROCESO', 'equipo': self.equipo_mes.pk, 'tecnico': self.tecnico.pk,
        })
        self.assertRedirects(r, reverse('lista_tickets'))
        self.ticket.refresh_from_db()
        self.assertEqual((self.ticket.prioridad, self.ticket.estado), ('ALTA', 'EN_PROCESO'))

        r = self.client.post(reverse('eliminar_ticket', args=[self.ticket.pk]))
        self.assertRedirects(r, reverse('lista_tickets'))
        self.assertFalse(TicketSoporte.objects.filter(pk=self.ticket.pk).exists())


class ConsultasN1Tests(DatosBase):
    """El número de consultas de los listados no debe crecer con la cantidad de registros (sin N+1)."""

    def agregar_registros(self, n):
        inicio = Producto.objects.count()
        for i in range(inicio, inicio + n):
            p = Producto.objects.create(
                codigo_sku=f'EXTRA-{i}', nombre=f'Extra {i}', marca='X', modelo='Y',
                precio_base=Decimal('1.00'), meses_garantia=12, categoria=self.categoria,
            )
            Suministro.objects.create(producto=p, proveedor=self.proveedor, precio_compra=Decimal('1.00'),
                                      dias_entrega_promedio=1)
            equipo = EquipoInstalado.objects.create(
                numero_serie=f'EXTRA-{i}', producto=p, cliente=self.cliente,
                fecha_instalacion=date(2024, 1, 1), fin_garantia=date(2025, 1, 1),
            )
            TicketSoporte.objects.create(codigo_ticket=f'EXTRA-{i}', descripcion_falla='-', equipo=equipo,
                                         tecnico=self.tecnico)

    def test_productos_proveedores_3_consultas(self):
        # producto + categoria (JOIN) | suministros | proveedores
        for extra in (1, 10):
            self.agregar_registros(extra)
            with self.subTest(productos=Producto.objects.count()), self.assertNumQueries(3):
                self.client.get(reverse('productos_proveedores'))

    def test_lista_tickets_1_consulta(self):
        # ticket + equipo + cliente + tecnico en un solo SELECT con JOINs
        for extra in (1, 10):
            self.agregar_registros(extra)
            with self.subTest(tickets=TicketSoporte.objects.count()), self.assertNumQueries(1):
                self.client.get(reverse('lista_tickets'))


class ReportePostventaTests(DatosBase):

    def test_reporte_postventa(self):
        Suministro.objects.create(producto=self.monitor, proveedor=self.proveedor, precio_compra=Decimal('800.00'),
                                  dias_entrega_promedio=10, es_proveedor_principal=True)
        Suministro.objects.create(producto=self.ventilador, proveedor=self.proveedor, precio_compra=Decimal('4000.00'),
                                  dias_entrega_promedio=21)

        r = self.client.get(reverse('reporte_postventa'))
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'inventario/base.html')

        # aggregate(): un equipo con garantía vigente (instalado hoy) y otro vencida (enero 2026)
        garantias = r.context['garantias']
        self.assertEqual((garantias['total'], garantias['vigentes'], garantias['vencidas']), (2, 1, 1))
        self.assertEqual(garantias['pct_vigentes'], 50)
        self.assertEqual((r.context['tickets']['total'], r.context['tickets']['pendientes']), (1, 1))

        # annotate(): el técnico tiene el ticket abierto
        tecnico = r.context['tecnicos'][0]
        self.assertEqual((tecnico.asignados, tecnico.pendientes, tecnico.atendidos), (1, 1, 0))
        cliente = r.context['clientes'][0]
        self.assertEqual((cliente.equipos_total, cliente.garantia_vencida, cliente.tickets_pendientes), (2, 1, 1))

        # values().annotate()
        self.assertEqual(r.context['por_prioridad'][0]['prioridad'], 'MEDIA')
        proveedor = r.context['proveedores'][0]
        self.assertEqual((proveedor['productos'], proveedor['como_principal'], proveedor['dias_entrega']), (2, 1, 15.5))
        self.assertContains(r, '15.5 días')  # floatformat:1 sobre el Avg


class TicketSoporteQuerySetTests(DatosBase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        # TCK-1 (de DatosBase): MEDIA, ABIERTO, con técnico
        cls.critico = TicketSoporte.objects.create(codigo_ticket='TCK-2', descripcion_falla='No enciende',
                                                   equipo=cls.equipo_mes, prioridad='CRITICA', estado='EN_PROCESO')
        cls.alta_resuelto = TicketSoporte.objects.create(codigo_ticket='TCK-3', descripcion_falla='Calibración',
                                                         equipo=cls.equipo_antiguo, prioridad='ALTA',
                                                         estado='RESUELTO', tecnico=cls.tecnico)
        # Un ticket de un mes anterior (auto_now_add no deja fijar la fecha al crear)
        cls.antiguo = TicketSoporte.objects.create(codigo_ticket='TCK-4', descripcion_falla='Ruido',
                                                   equipo=cls.equipo_antiguo, prioridad='BAJA', estado='CERRADO')
        TicketSoporte.objects.filter(pk=cls.antiguo.pk).update(fecha_creacion=timezone.now() - timedelta(days=60))

    def codigos(self, qs):
        return sorted(qs.values_list('codigo_ticket', flat=True))

    def test_reglas_basicas(self):
        self.assertEqual(self.codigos(TicketSoporte.objects.pendientes()), ['TCK-1', 'TCK-2'])
        self.assertEqual(self.codigos(TicketSoporte.objects.atendidos()), ['TCK-3', 'TCK-4'])
        self.assertEqual(self.codigos(TicketSoporte.objects.urgentes()), ['TCK-2', 'TCK-3'])
        self.assertEqual(self.codigos(TicketSoporte.objects.sin_tecnico()), ['TCK-2', 'TCK-4'])
        self.assertEqual(self.codigos(TicketSoporte.objects.de_tecnico(self.tecnico)), ['TCK-1', 'TCK-3'])
        self.assertEqual(self.codigos(TicketSoporte.objects.creados_en_mes()), ['TCK-1', 'TCK-2', 'TCK-3'])

    def test_metodos_encadenables(self):
        self.assertEqual(self.codigos(TicketSoporte.objects.pendientes().urgentes()), ['TCK-2'])
        self.assertEqual(self.codigos(TicketSoporte.objects.pendientes().urgentes().sin_tecnico()), ['TCK-2'])
        self.assertEqual(self.codigos(TicketSoporte.objects.atendidos().urgentes().de_tecnico(self.tecnico)), ['TCK-3'])
        self.assertEqual(self.codigos(TicketSoporte.objects.filter(equipo=self.equipo_mes).pendientes()), ['TCK-1', 'TCK-2'])

    def test_con_detalle_una_sola_consulta(self):
        with self.assertNumQueries(1):
            [(t.equipo.cliente.razon_social, t.tecnico) for t in TicketSoporte.objects.con_detalle().recientes()]

    def test_q_con_prefijo_desde_otro_modelo(self):
        T = TicketSoporteQuerySet
        tecnico = Usuario.objects.annotate(
            pendientes=Count('tickets_asignados', filter=T.q_pendiente('tickets_asignados__')),
        ).get(pk=self.tecnico.pk)
        self.assertEqual(tecnico.pendientes, 1)

    def test_lista_tickets_vistas(self):
        casos = {
            '': ['TCK-1', 'TCK-2', 'TCK-3', 'TCK-4'],
            '?vista=pendientes': ['TCK-1', 'TCK-2'],
            '?vista=urgentes': ['TCK-2'],
            '?vista=sin_tecnico': ['TCK-2'],
            '?vista=mes': ['TCK-1', 'TCK-2', 'TCK-3'],
            '?vista=atendidos': ['TCK-3', 'TCK-4'],
            '?vista=pendientes&prioridad=MEDIA': ['TCK-1'],
        }
        for query, esperado in casos.items():
            with self.subTest(query=query):
                r = self.client.get(reverse('lista_tickets') + query)
                self.assertEqual(r.status_code, 200)
                self.assertEqual(sorted(t.codigo_ticket for t in r.context['tickets']), esperado)

    def test_reporte_postventa_usa_queryset(self):
        r = self.client.get(reverse('reporte_postventa'))
        self.assertEqual([t.codigo_ticket for t in r.context['urgentes_pendientes']], ['TCK-2'])
        self.assertEqual((r.context['tickets']['pendientes'], r.context['tickets']['criticos_pendientes'],
                          r.context['tickets']['sin_tecnico']), (2, 1, 1))
        tecnico = r.context['tecnicos'][0]
        self.assertEqual((tecnico.asignados, tecnico.pendientes, tecnico.urgentes, tecnico.atendidos), (2, 1, 0, 1))


class EditarTicketConsultasTests(DatosBase):
    """El desplegable de equipos del formulario de ticket no debe hacer 1 consulta por equipo (N+1)."""

    def test_editar_ticket_consultas_constantes(self):
        url = reverse('editar_ticket', args=[self.ticket.pk])
        for extra in (0, 20):
            for i in range(extra):
                cliente = Cliente.objects.create(
                    razon_social=f'Cliente {i}', numero_identificacion=f'X{i}', email_contacto=f'c{i}@x.pe',
                    telefono='0', direccion_fiscal='-',
                )
                EquipoInstalado.objects.create(numero_serie=f'EXTRA-{i}', producto=self.monitor, cliente=cliente,
                                               fecha_instalacion=date(2024, 1, 1), fin_garantia=date(2026, 1, 1))
            # ticket | equipos + cliente (JOIN) | técnicos
            with self.subTest(equipos=EquipoInstalado.objects.count()), self.assertNumQueries(3):
                r = self.client.get(url)
            self.assertContains(r, 'Serie: MON-0001 - Clínica San Gabriel')
