from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.db.models import Prefetch
from django.test.utils import override_settings

from inventario.models import Cliente, EquipoInstalado
from inventario.serializer import ClienteConEquiposSerializer


class Command(BaseCommand):
    help = "Ejercicio 7: mide consultas al serializar Clientes con equipos anidados (antes vs. después)."

    def medir(self, queryset):
        with override_settings(DEBUG=True):  # connection.queries solo registra con DEBUG=True
            reset_queries()
            datos = ClienteConEquiposSerializer(queryset, many=True).data
            list(datos)  # fuerza la serialización completa
            return len(connection.queries), len(datos)

    def handle(self, *args, **opts):
        antes, n = self.medir(Cliente.objects.all())
        despues, _ = self.medir(
            Cliente.objects.prefetch_related(
                Prefetch('equipos', queryset=EquipoInstalado.objects.select_related('producto'))
            )
        )
        self.stdout.write(f"Clientes serializados: {n}")
        self.stdout.write(f"ANTES   (Cliente.objects.all())      : {antes} consultas")
        self.stdout.write(f"DESPUÉS (prefetch + select_related)  : {despues} consultas")
