# Laboratorio 13 — Ejercicio 1: Reconocer el tipo de comercio y los canales

## Tipos de comercio electrónico

| Tipo | Quién vende a quién | Ejemplo peruano |
|---|---|---|
| B2C (Business to Consumer) | Una empresa vende a consumidores finales (personas). | Inkafarma (inkafarma.pe): la cadena de farmacias vende medicamentos y productos de cuidado personal a las personas con entrega a domicilio. |
| B2B (Business to Business) | Una empresa vende a otras empresas, normalmente en grandes volúmenes y con precios por cliente. | Makro Perú: mayorista que abastece a bodegas, restaurantes y otros negocios. |
| C2C (Consumer to Consumer) | Un consumidor vende a otro consumidor; la plataforma solo pone el espacio y cobra una comisión. | Mercado Libre Perú: en su marketplace, personas publican y venden artículos usados o propios a otras personas. |

## ¿De qué tipo es la cafetería en línea de la práctica?

Es **B2C**: la cafetería (una empresa) vende café y postres directamente a clientes finales (personas) que compran para consumir ellos mismos. El cliente se registra, arma un carrito y paga su pedido.

## Canales que pueden usar la misma API de Django

| Canal | Cómo llega el cliente | ¿Usa la misma API de Django? |
|---|---|---|
| Web (React) | Navegador en computadora o celular | Sí: pide `/api/productos/` con Axios |
| App móvil (m-commerce) | Aplicación en el celular, con la misma tienda | Sí: mismas rutas y mismo JSON; solo cambia la pantalla |
| Redes sociales (social commerce) | Catálogo y pedidos desde Instagram o WhatsApp Business | Sí: un enlace o bot consulta la misma API o recibe pedidos por ella |

La API entrega y valida datos en JSON y no sabe quién la llama; por eso los tres canales comparten el mismo catálogo, las mismas reglas de precio y stock y la misma base de datos.

## Por qué m-commerce y social commerce son un canal y no un tipo de comercio

El **tipo** de comercio responde a «¿quién le vende a quién?» (empresa a persona, empresa a empresa o persona a persona). El **canal** responde a «¿por dónde se realiza la compra?». M-commerce significa comprar desde el celular, y social commerce, comprar dentro de una red social; en ninguno de los dos cambia quién vende y quién compra. La cafetería sigue siendo B2C tanto si el cliente compra desde la web, desde la app o desde Instagram. Por eso el mismo negocio puede usar varios canales a la vez con una sola API y una sola base de datos.

## Capturas

- `01_tipos_comercio.png` — tabla de tipos de comercio con ejemplos peruanos.
- `02_canales.png` — tabla de canales que comparten la API de la cafetería.
