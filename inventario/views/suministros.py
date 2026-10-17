from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404

from ..forms import SuministroForm
from ..models import Producto, Suministro


# CRUD del modelo intermedio de la relación N:M (Producto <-> Proveedor vía Suministro)

# Vista para Crear un Suministro (agregar un Proveedor a un Producto, con sus atributos propios)
def crear_suministro(request, producto_pk):
    producto = get_object_or_404(Producto, pk=producto_pk)

    if request.method == 'POST':
        form = SuministroForm(request.POST)
        if form.is_valid():
            suministro = form.save(commit=False)
            suministro.producto = producto
            try:
                suministro.save()
                return redirect('productos_proveedores')
            except IntegrityError:
                form.add_error('proveedor', 'Este proveedor ya está registrado para este producto.')
    else:
        form = SuministroForm()

    return render(request, 'inventario/crear_suministro.html', {'form': form, 'producto': producto})


# Vista para Editar un Suministro (modificar los atributos propios de la relación N:M)
def editar_suministro(request, pk):
    suministro = get_object_or_404(Suministro, pk=pk)

    if request.method == 'POST':
        form = SuministroForm(request.POST, instance=suministro)
        if form.is_valid():
            try:
                form.save()
                return redirect('productos_proveedores')
            except IntegrityError:
                form.add_error('proveedor', 'Este proveedor ya está registrado para este producto.')
    else:
        form = SuministroForm(instance=suministro)

    return render(request, 'inventario/editar_suministro.html', {'form': form, 'objeto': suministro})


# Vista para Eliminar un Suministro (quitar un Proveedor de un Producto, con confirmación previa)
def eliminar_suministro(request, pk):
    suministro = get_object_or_404(Suministro, pk=pk)
    if request.method == 'POST':
        suministro.delete()
        return redirect('productos_proveedores')

    return render(request, 'inventario/eliminar_suministro.html', {'objeto': suministro})
