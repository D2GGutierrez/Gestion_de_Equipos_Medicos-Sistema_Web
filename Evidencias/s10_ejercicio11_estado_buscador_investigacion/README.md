# Laboratorio 10 – Ejercicio 11: Estado, eventos y buscador en la investigación propia

## Qué se hizo
**Botón con estado y evento de clic – `ProveedorCard`**
- `const [favorito, setFavorito] = useState(false)`: estado booleano propio de cada tarjeta (cada proveedor es favorito o no, de forma independiente).
- `<button onClick={() => setFavorito(!favorito)}>` invierte el valor en cada clic.
- Según el estado cambia el texto del botón («Marcar como favorito» / «Quitar de favoritos»), aparece «★ Favorito» (`&&`) y la tarjeta cambia de color (`className` condicional).

**Buscador controlado – `ListaProveedores`**
- `const [busqueda, setBusqueda] = useState('')` con `<input value={busqueda} onChange={(e) => setBusqueda(e.target.value)} />`.
- `proveedores.filter((p) => p.nombre_empresa.toLowerCase().includes(texto))` filtra por nombre de empresa sin distinguir mayúsculas y sin modificar el arreglo original.
- El título muestra la cantidad filtrada y, si no hay coincidencias, `Sin resultados para «texto»`.

## Antes y después de cada interacción
| Interacción | Antes | Después |
|---|---|---|
| Clic en «Marcar como favorito» de MedTech y de Distribuidora del Sur | 4 botones «Marcar como favorito», ninguna tarjeta resaltada | Esas dos tarjetas dicen «★ Favorito», con fondo verde y botón «Quitar de favoritos»; las otras dos no cambian |
| Segundo clic en MedTech («Quitar de favoritos») | Favorito | Vuelve a «Marcar como favorito», sin resaltar |
| Buscar `MEDTECH` (mayúsculas) | 4 proveedores | 1 proveedor: MedTech Perú S.A.C. |
| Buscar `sur` | 4 proveedores | 1 proveedor: Distribuidora Hospitalaria del Sur |
| Buscar `zzz` | 4 proveedores | 0 proveedores y «Sin resultados para «zzz»» |

## Detalle a tener en cuenta
Al filtrar, las tarjetas que salen de la lista se desmontan y pierden su estado de favorito (el estado vive en cada `ProveedorCard`); las que siguen visibles lo conservan por la `key={p.id}`.

## Verificación
- `npm run lint`: sin errores. `npm run build`: compila correctamente. Consola sin errores ni warnings.

## Capturas
- Código: `captura_codigo_ProveedorCard.jsx.png`, `captura_codigo_ListaProveedores.jsx.png`
- Clic: `captura_01_antes_clic.png`, `captura_02_despues_clic.png`
- Búsquedas: `captura_03_busqueda_MEDTECH.png`, `captura_04_busqueda_sur.png`, `captura_05_busqueda_zzz.png`
