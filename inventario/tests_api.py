"""Ejercicio 11 - Códigos de estado de la API (200, 201, 400, 404, 204) con el cliente de pruebas de DRF."""
from rest_framework import status
from rest_framework.test import APITestCase

from datetime import date

from .models import Categoria, Cliente, EquipoInstalado, Producto


class CodigosEstadoCategoriaTest(APITestCase):
    def setUp(self):
        self.cat = Categoria.objects.create(nombre='Monitoreo')

    def test_200_listar(self):
        r = self.client.get('/api/categorias/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_201_crear(self):
        r = self.client.post('/api/categorias/', {'nombre': 'Soporte Vital'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_400_dato_invalido(self):
        r = self.client.post('/api/categorias/', {'nombre': ''}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)

    def test_404_no_existe(self):
        r = self.client.get('/api/categorias/9999/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_204_eliminar(self):
        r = self.client.delete(f'/api/categorias/{self.cat.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)


class CodigosEstadoClienteTest(APITestCase):
    DATOS = dict(razon_social='Clínica Demo SAC', numero_identificacion='20512345678',
                 email_contacto='demo@clinica.pe', telefono='014000000', direccion_fiscal='Av. Lima 123')

    def setUp(self):
        self.cli = Cliente.objects.create(**{**self.DATOS, 'numero_identificacion': '20111111111'})

    def test_200_detalle(self):
        r = self.client.get(f'/api/clientes/{self.cli.pk}/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)

    def test_200_actualizar(self):
        r = self.client.patch(f'/api/clientes/{self.cli.pk}/', {'telefono': '999888777'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['telefono'], '999888777')

    def test_201_crear(self):
        r = self.client.post('/api/clientes/', self.DATOS, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)

    def test_400_ruc_invalido(self):
        r = self.client.post('/api/clientes/', {**self.DATOS, 'numero_identificacion': '123'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_identificacion', r.data)

    def test_404_no_existe(self):
        r = self.client.get('/api/clientes/9999/')
        self.assertEqual(r.status_code, status.HTTP_404_NOT_FOUND)

    def test_204_eliminar(self):
        r = self.client.delete(f'/api/clientes/{self.cli.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cliente.objects.filter(pk=self.cli.pk).exists())


class CodigosEstadoEquipoTest(APITestCase):
    """Lab 12 Ej 9 - API de EquipoInstalado: CRUD, validaciones (400) y parámetros de búsqueda."""

    def setUp(self):
        self.cli = Cliente.objects.create(razon_social='Clinica Uno', numero_identificacion='20111111111',
                                          email_contacto='a@a.pe', telefono='1', direccion_fiscal='x')
        self.prod = Producto.objects.create(codigo_sku='SKU-1', nombre='Monitor Multiparametro', marca='M', modelo='X',
                                            precio_base=100, meses_garantia=12, stock=1)
        self.eq = EquipoInstalado.objects.create(numero_serie='MON-0001', fecha_instalacion=date(2026, 1, 1),
                                                 fin_garantia=date(2027, 1, 1), estado='OPERATIVO',
                                                 producto=self.prod, cliente=self.cli)
        self.DATOS = {'numero_serie': 'ECO-0001', 'fecha_instalacion': '2026-02-01', 'fin_garantia': '2027-02-01',
                      'estado': 'OPERATIVO', 'producto': self.prod.pk, 'cliente': self.cli.pk}

    def test_200_listar_y_detalle(self):
        self.assertEqual(self.client.get('/api/equipos/').status_code, status.HTTP_200_OK)
        self.assertEqual(self.client.get(f'/api/equipos/{self.eq.pk}/').status_code, status.HTTP_200_OK)

    def test_201_crear(self):
        r = self.client.post('/api/equipos/', self.DATOS, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['producto_nombre'], 'Monitor Multiparametro')

    def test_201_normaliza_serie_a_mayusculas(self):
        r = self.client.post('/api/equipos/', {**self.DATOS, 'numero_serie': ' eco-0002 '}, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        self.assertEqual(r.data['numero_serie'], 'ECO-0002')

    def test_400_formato_de_serie(self):
        r = self.client.post('/api/equipos/', {**self.DATOS, 'numero_serie': 'ABC'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_serie', r.data)

    def test_400_serie_duplicada_aunque_cambie_la_capitalizacion(self):
        r = self.client.post('/api/equipos/', {**self.DATOS, 'numero_serie': 'mon-0001'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('numero_serie', r.data)

    def test_400_garantia_antes_de_la_instalacion(self):
        r = self.client.post('/api/equipos/', {**self.DATOS, 'fin_garantia': '2025-01-01'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('fin_garantia', r.data)

    def test_200_patch_estado_y_conserva_serie(self):
        r = self.client.patch(f'/api/equipos/{self.eq.pk}/', {'estado': 'MANTENIMIENTO'}, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data['numero_serie'], 'MON-0001')

    def test_404_no_existe(self):
        self.assertEqual(self.client.get('/api/equipos/9999/').status_code, status.HTTP_404_NOT_FOUND)

    def test_204_eliminar(self):
        r = self.client.delete(f'/api/equipos/{self.eq.pk}/')
        self.assertEqual(r.status_code, status.HTTP_204_NO_CONTENT)

    def test_parametros_search_estado_y_ordering(self):
        self.client.post('/api/equipos/', {**self.DATOS, 'estado': 'INACTIVO'}, format='json')
        self.assertEqual(len(self.client.get('/api/equipos/?search=MON-00').data), 1)
        self.assertEqual(len(self.client.get('/api/equipos/?estado=INACTIVO').data), 1)
        self.assertEqual(len(self.client.get(f'/api/equipos/?cliente={self.cli.pk}').data), 2)
        series = [e['numero_serie'] for e in self.client.get('/api/equipos/?ordering=-numero_serie').data]
        self.assertEqual(series, ['MON-0001', 'ECO-0001'])


class ProductoSoloLecturaTest(APITestCase):
    """Lab 12 Ej 11 - /api/productos/ es de solo lectura."""

    def setUp(self):
        self.prod = Producto.objects.create(codigo_sku='SKU-9', nombre='Monitor', marca='M', modelo='X',
                                            precio_base=100, meses_garantia=24, stock=1)

    def test_200_listar_con_meses_de_garantia(self):
        r = self.client.get('/api/productos/')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual(r.data[0]['meses_garantia'], 24)

    def test_405_no_permite_crear_ni_borrar(self):
        self.assertEqual(self.client.post('/api/productos/', {}, format='json').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(self.client.delete(f'/api/productos/{self.prod.pk}/').status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
