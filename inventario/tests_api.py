"""Ejercicio 11 - Códigos de estado de la API (200, 201, 400, 404, 204) con el cliente de pruebas de DRF."""
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Categoria, Cliente


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
