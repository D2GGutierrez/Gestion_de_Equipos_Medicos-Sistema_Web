from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import (
    Categoria, Cliente, EquipoInstalado, Producto, Proveedor, Suministro, TicketSoporte, Usuario,
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
