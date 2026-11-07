# Laboratorio 10 – Ejercicio 4: Componente contenedor con `children`

## Qué se hizo
- Nuevo componente `Tarjeta` (`src/components/Tarjeta.jsx`): recibe `titulo` por props y `children`.
- En `App.jsx` las tres secciones (catálogo, prueba del valor por defecto y clientes) quedan **envueltas** en `<Tarjeta titulo="...">...</Tarjeta>`; lo que va entre las etiquetas llega como `children`.
- Estilos nuevos en `App.css`: `.panel` y `.panel-titulo` (la clase `.tarjeta` ya se usa para cada ítem de la lista, por eso el contenedor usa otro nombre de clase).
- `ListaProductos` pasa su encabezado a `<h3>` porque ahora el `<h2>` lo pone `Tarjeta`.

## ¿Qué es `children`? (equivalente en Django)
`children` es el contenido que el padre escribe entre la etiqueta de apertura y de cierre del componente. En los templates de Django el equivalente es la herencia con bloques: `base.html` define el marco (como `Tarjeta`) con `{% block content %}{% endblock %}` y cada página rellena ese bloque. Aquí `{children}` ocupa el lugar del `{% block %}`, y `titulo` sería una variable de contexto (`{{ titulo }}`).

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente.
- Consola del navegador: sin warnings ni errores (solo mensajes informativos de Vite/DevTools).
- 3 paneles renderizados: "Catálogo de productos", "Prueba del valor por defecto", "Clientes y sus equipos instalados".

## Capturas
- `captura_codigo_Tarjeta.jsx.png`, `captura_codigo_App.jsx.png`
- `captura_pagina_antes.png` (Ej. 3) y `captura_pagina_resultado.png` (Ej. 4)
