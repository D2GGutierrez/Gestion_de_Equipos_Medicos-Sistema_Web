from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from ..forms import UsuarioForm
from ..models import Usuario


# Vista para Listar Usuarios del sistema
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by('nombre_completo')

    rol = request.GET.get('rol')
    if rol:
        usuarios = usuarios.filter(rol=rol)

    return render(request, 'inventario/lista_usuarios.html', {
        'usuarios': usuarios,
        'roles': Usuario.ROLES,
        'rol_seleccionado': rol,
    })


# Vista para Actualizar un Usuario (UPDATE mediante ORM)
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('lista_usuarios')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'inventario/form_generico.html', {
        'form': form, 'titulo': f'Editar Usuario: {usuario}', 'url_cancelar': reverse('lista_usuarios'),
    })


# Vista para Eliminar un Usuario (DELETE mediante ORM, con confirmacion previa)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        return redirect('lista_usuarios')

    return render(request, 'inventario/confirmar_eliminar.html', {
        'objeto': usuario, 'titulo_entidad': 'Usuario', 'url_cancelar': reverse('lista_usuarios'),
    })
