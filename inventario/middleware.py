from django.conf import settings
from django.db import connection, reset_queries


# Solo para desarrollo: muestra en cada página HTML cuántas consultas SQL ejecutó la petición.
# connection.queries solo registra consultas con DEBUG=True, así que en producción no hace nada.
class ContadorConsultasMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            return self.get_response(request)

        reset_queries()
        response = self.get_response(request)

        es_html = response.get('Content-Type', '').startswith('text/html')
        if es_html and not response.streaming and b'</body>' in response.content:
            total = len(connection.queries)
            insignia = (
                f'<div id="contador-consultas" style="position:fixed;bottom:12px;right:12px;z-index:9999;'
                f'background:#212529;color:#fff;padding:8px 14px;border-radius:8px;font:600 15px system-ui;'
                f'box-shadow:0 2px 8px rgba(0,0,0,.3)">Consultas SQL: {total}</div>'
            ).encode()
            response.content = response.content.replace(b'</body>', insignia + b'</body>', 1)
            response['Content-Length'] = len(response.content)
        return response
