from django import forms
from bibliotecas.models import Biblioteca
from registros.models import Registro  # Importación correcta entre apps Django
from .models import Fiador

class FiadorForm(forms.Form):
    nombres = forms.CharField(max_length=255, label="Nombre del Fiador")
    apellido_paterno = forms.CharField(max_length=255, label="Apellido Paterno del Fiador")
    apellido_materno = forms.CharField(max_length=255, label="Apellido Materno del Fiador")
    domicilio = forms.CharField(max_length=255, label="Domicilio del Fiador")
    codigo_postal = forms.CharField(max_length=10, label="Código Postal del Fiador")
    telefono = forms.CharField(max_length=20, label="Teléfono del Fiador")
    email = forms.EmailField(label="Correo electrónico del Fiador")
    ocupacion = forms.CharField(max_length=255, label="Ocupación del Fiador")
    nombre_direccion_trabajo = forms.CharField(max_length=255, label="Nombre de la dirección de trabajo del Fiador")
    telefono_trabajo = forms.CharField(max_length=20, label="Teléfono de trabajo del Fiador")
    role = forms.CharField(max_length=50, label="Rol del Fiador")
    responsabilidad = forms.BooleanField(label="Responsabilidad del Fiador")
    retraso = forms.CharField(max_length=255, label="Retraso del Fiador")
    suspension = forms.CharField(max_length=255, label="Suspensión del Fiador")
    aviso_usuario = forms.CharField(max_length=255, label="Aviso al Usuario del Fiador")
    created_at = forms.DateTimeField(label="Fecha de Creación del Fiador")
    updated_at = forms.DateTimeField(label="Fecha de Actualización del Fiador")
    biblioteca = forms.ModelChoiceField(queryset=Biblioteca.objects.all(), label="Biblioteca del Fiador")
    registro = forms.ModelChoiceField(queryset=Registro.objects.all(), label="Registro del Fiador") # Importación absoluta

    def __str__(self):
        return self.nombres