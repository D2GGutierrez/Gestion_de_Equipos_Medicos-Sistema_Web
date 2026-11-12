# Laboratorio 11 – Ejercicio 7: Hermanos que comparten un filtro

## Qué se hizo
- **`Buscador.jsx`** (nuevo): campo de texto **controlado**. Recibe `valor` y `onCambiar` por props: `value={valor}` y `onChange={(e) => onCambiar(e.target.value)}`. No guarda el texto, solo avisa cada cambio.
- **`Practica.jsx`** (padre): guarda el texto en `const [busqueda, setBusqueda] = useState('')` y filtra **antes** de entregar los datos:
  `productos.filter((p) => p.nombre.toLowerCase().includes(texto))` (con `toLowerCase()` para no distinguir mayúsculas y sin modificar el arreglo original). Pasa `valor={busqueda}` y `onCambiar={setBusqueda}` a `Buscador`, y los `productosFiltrados` a `Catalogo`.
- **`Catalogo.jsx`**: muestra `No hay productos que coincidan` con `&&` cuando recibe un arreglo vacío.

## Búsquedas documentadas
| Búsqueda | Catálogo |
|---|---|
| (vacío) | 5 productos |
| `ca` | **2**: Café americano y Capuchino |
| `zzz` | 0 productos y el mensaje «No hay productos que coincidan» |
| `CAPU` (mayúsculas) | 1: Capuchino |
| se borra el texto | vuelven los 5 |

Detalle útil: al filtrar, el **carrito no se pierde** (se agregó un Café americano estando filtrado y quedó en el carrito), porque su estado vive en `Practica` y no en las tarjetas que se ocultan; en el Laboratorio 10 las tarjetas filtradas perdían su contador porque el estado vivía en cada tarjeta.

## ¿Por qué `Buscador` y `Catalogo` no se comunican directamente?
Son **hermanos**: ninguno es padre o hijo del otro y en React los datos solo viajan hacia abajo por props. `Buscador` no puede llamar a `Catalogo` ni leer su contenido. Por eso el camino es: el usuario escribe en `Buscador` → este avisa al padre con `onCambiar` → `Practica` guarda el texto en su estado y filtra → entrega a `Catalogo` solo los productos que coinciden. Así hay una sola fuente de verdad (el texto en el padre) y los hermanos quedan independientes: `Catalogo` solo muestra lo que recibe y no sabe de dónde sale el filtro.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola del navegador sin errores ni warnings.

## Capturas
`captura_codigo_Practica.jsx.png`, `captura_codigo_Buscador.jsx.png`, `captura_codigo_Catalogo.jsx.png`, `captura_00_sin_busqueda.png`, `captura_01_busqueda_ca.png`, `captura_02_busqueda_zzz.png`
