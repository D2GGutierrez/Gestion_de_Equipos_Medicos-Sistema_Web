from django import forms
from .models import Producto, Cliente, Usuario, EquipoInstalado, TicketSoporte, Suministro


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['codigo_sku',
                    'nombre',
                    'marca',
                    'modelo',
                    'precio_base',
                    'meses_garantia',
                    'stock',
                    'categoria',
                ]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['razon_social', 'numero_identificacion', 'email_contacto', 'telefono', 'direccion_fiscal', 'activo']


class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre_completo', 'email', 'rol', 'activo']


class EquipoInstaladoForm(forms.ModelForm):
    class Meta:
        model = EquipoInstalado
        fields = ['numero_serie', 'fecha_instalacion', 'fin_garantia', 'estado', 'producto', 'cliente']
        widgets = {
            'fecha_instalacion': forms.DateInput(attrs={'type': 'date'}),
            'fin_garantia': forms.DateInput(attrs={'type': 'date'}),
        }


class TicketSoporteForm(forms.ModelForm):
    class Meta:
        model = TicketSoporte
        fields = ['codigo_ticket', 'descripcion_falla', 'prioridad', 'estado', 'equipo', 'tecnico']


# Formulario del modelo intermedio de la relación N:M (Producto <-> Proveedor).
# 'producto' no se incluye: se fija desde la vista según el producto sobre el que se opera.
class SuministroForm(forms.ModelForm):
    class Meta:
        model = Suministro
        fields = ['proveedor', 'precio_compra', 'dias_entrega_promedio', 'es_proveedor_principal']


# Formulario de la operación "Registrar Instalación": no es un ModelForm porque una sola
# operación crea varios EquipoInstalado y descuenta el stock del Producto.
class RegistrarInstalacionForm(forms.Form):
    producto = forms.ModelChoiceField(queryset=Producto.objects.order_by('nombre'))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.filter(activo=True).order_by('razon_social'))
    fecha_instalacion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    numeros_serie = forms.CharField(
        label='Números de serie',
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text='Uno por línea. La cantidad de equipos a instalar es la cantidad de series.',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Muestra el stock disponible en cada opción del desplegable
        self.fields['producto'].label_from_instance = lambda p: f'{p.nombre} - {p.modelo} (stock: {p.stock})'
        for field in self.fields.values():
            es_select = isinstance(field.widget, forms.Select)
            field.widget.attrs['class'] = 'form-select' if es_select else 'form-control'

    def clean_numeros_serie(self):
        series = [s.strip() for s in self.cleaned_data['numeros_serie'].splitlines() if s.strip()]
        if len(series) != len(set(series)):
            raise forms.ValidationError('Hay números de serie repetidos.')
        existentes = list(EquipoInstalado.objects.filter(numero_serie__in=series).values_list('numero_serie', flat=True))
        if existentes:
            raise forms.ValidationError(f'Ya están registrados: {", ".join(existentes)}.')
        return series
