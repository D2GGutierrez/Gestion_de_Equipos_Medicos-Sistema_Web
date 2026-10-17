from django.core.management.base import BaseCommand
from django.db import connection, reset_queries
from django.test.utils import override_settings

from inventario.models import TicketSoporte
from inventario.serializer import TicketDetalleSerializer


class Command(BaseCommand):
    help = "Ejercicio 12: consultas al serializar Tickets con equipo/cliente/producto/técnico anidados."

    def medir(self, queryset):
        with override_settings(DEBUG=True):  # connection.queries solo registra con DEBUG=True
            reset_queries()
            datos = TicketDetalleSerializer(queryset, many=True).data
            list(datos)
            return len(connection.queries), len(datos)

    def handle(self, *args, **opts):
        antes, n = self.medir(TicketSoporte.objects.all())
        despues, _ = self.medir(
            TicketSoporte.objects.select_related('equipo__cliente', 'equipo__producto', 'tecnico')
        )
        self.stdout.write(f"Tickets serializados: {n}")
        self.stdout.write(f"ANTES   (TicketSoporte.objects.all()) : {antes} consultas")
        self.stdout.write(f"DESPUÉS (select_related)              : {despues} consultas")
