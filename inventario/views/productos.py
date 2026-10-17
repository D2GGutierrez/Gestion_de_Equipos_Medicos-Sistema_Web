from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import ProductoForm
from ..models import Categoria, Producto, ProductoQuerySet


# Vista para Listar Productos (Optimizado con select_related para 1:1 y 1:N)
# Filtros por regla de negocio con los métodos encadenables de ProductoQuerySet
def lista_productos(request):
    productos = Producto.objects.con_detalle()

    stock = request.GET.get('stock')
    if stock == 'disponibles':
        productos = productos.disponibles()
    elif stock == 'bajo':
        productos = productos.stock_bajo()
    elif stock == 'agotados':
        productos = productos.agotados()

    instalados_mes = request.GET.get('mes') == 'actual'
    if instalados_mes:
        productos = productos.instalados_en_mes()

    return render(request, 'inventario/lista_productos.html', {
        'productos': productos.por_nombre(),
        'stock_seleccionado': stock,
        'instalados_mes': instalados_mes,
        'stock_minimo': ProductoQuerySet.STOCK_MINIMO,
    })


# Vista para Consultar Productos con Proveedores (Optimizado con prefetch_related para N:M con modelo intermedio)
def productos_proveedores(request):
    # select_related: la Categoría (FK, un objeto por producto) viene en el mismo SELECT con un JOIN.
    # prefetch_related: los Suministros (lado "muchos") y sus Proveedores llegan en 1 consulta extra cada uno.
    # Total: 3 consultas sin importar cuántos productos haya (antes: 1 + 1 por producto para la categoría).
    productos = Producto.objects.select_related('categoria').prefetch_related(
        'suministro_set__proveedor'
    ).por_nombre()

    return render(request, 'inventario/productos_proveedores.html', {'productos': productos})


# Vista para Crear un Producto (CREATE mediante ORM)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda en SQLite usando Django ORM
            return redirect('lista_productos')  # Redirige al listado
    else:
        form = ProductoForm()

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': 'Registrar Nuevo Producto Médico', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Actualizar un Producto (UPDATE mediante ORM)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()  # UPDATE en SQLite usando Django ORM
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Producto: {producto}', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Eliminar un Producto (DELETE mediante ORM, con confirmacion previa)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()  # DELETE en SQLite usando Django ORM
        return redirect('lista_productos')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': producto, 'titulo_entidad': 'Producto', 'url_cancelar': reverse('lista_productos'),
    })


# Vista para Consultar una Categoría y listar sus Productos (Acceso Inverso via related_name)
def detalle_categoria(request, pk):
    """
    Usa prefetch_related('productos') para traer en una consulta optimizada
    la Categoría y todos los Productos asociados a ella (Acceso Inverso).
    """
    categoria = get_object_or_404(
        Categoria.objects.prefetch_related('productos'),
        pk=pk
    )

    return render(request, 'inventario/detalle_categoria.html', {
        'categoria': categoria
    })
