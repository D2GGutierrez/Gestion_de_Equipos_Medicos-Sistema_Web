from django.contrib import admin
from .models import (Cliente,Categoria,Proveedor,Producto,Usuario,
    EquipoInstalado,TicketSoporte,FichaTecnica,Suministro,)

class FichaTecnicaInline(admin.StackedInline):
    model = FichaTecnica
    extra = 0
    can_delete = False

class SuministroInline(admin.TabularInline):
    model = Suministro
    extra = 1
    fields = ('proveedor', 'precio_compra', 'dias_entrega_promedio', 'es_proveedor_principal')

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('codigo_sku', 'nombre', 'marca', 'modelo', 'precio_base', 'categoria')
    list_filter = ('categoria', 'marca')
    search_fields = ('codigo_sku', 'nombre', 'marca', 'modelo')
    inlines = [FichaTecnicaInline, SuministroInline]

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('razon_social', 'numero_identificacion', 'email_contacto', 'telefono', 'activo')
    list_filter = ('activo',)
    search_fields = ('razon_social', 'numero_identificacion', 'email_contacto')

@admin.register(TicketSoporte)
class TicketSoporteAdmin(admin.ModelAdmin):
    list_display = ('codigo_ticket', 'equipo', 'tecnico', 'prioridad', 'estado', 'fecha_creacion')
    list_filter = ('estado', 'prioridad')
    search_fields = ('codigo_ticket', 'descripcion_falla')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'email', 'rol', 'activo')
    list_filter = ('rol', 'activo')
    search_fields = ('nombre_completo', 'email')

@admin.register(EquipoInstalado)
class EquipoInstaladoAdmin(admin.ModelAdmin):
    list_display = ('numero_serie', 'producto', 'cliente', 'estado', 'fecha_instalacion', 'fin_garantia')
    list_filter = ('estado',)
    search_fields = ('numero_serie',)

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('nombre_empresa', 'ruc_nit', 'contacto', 'telefono')
    search_fields = ('nombre_empresa', 'ruc_nit')

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
