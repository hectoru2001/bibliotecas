# registros/forms.py
from django import forms
from django.contrib.auth.hashers import make_password
from bibliotecas.models import Biblioteca
from .models import Registro, UserRole

class RegistroForm(forms.ModelForm):
    confirm_password = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Registro
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno','curp','edad',
            'domicilio', 'codigo_postal', 'telefono', 'email', 'username',
            'password', 'ocupacion', 'escuela_trabajo', 'telefono_escuela_trabajo',
            'role', 'biblioteca', 'is_active', 'is_staff'
        ]
        widgets = {
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_paterno': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido_materno': forms.TextInput(attrs={'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'placeholder': 'CURP', 'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'nombres': forms.TextInput(attrs={'class': 'form-control'}),
            'ocupacion': forms.TextInput(attrs={'class': 'form-control'}),
            'escuela_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono_escuela_trabajo': forms.TextInput(attrs={'class': 'form-control'}),
            'biblioteca': forms.Select(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(),
        }
    

    def __init__(self, *args, **kwargs):
        # Obtener el usuario autenticado para limitar las bibliotecas
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Limitar las opciones de biblioteca según el usuario
        if self.user and not self.user.is_superuser:
            self.fields['biblioteca'].queryset = Biblioteca.objects.filter(id=self.user.biblioteca.id)
        else:
            self.fields['biblioteca'].queryset = Biblioteca.objects.all()


    def clean(self):
        cleaned = super().clean()
        password = cleaned.get('password')
        confirm = cleaned.get('confirm_password')
        role = cleaned.get('role')

        # Validar password confirm
        if password and confirm and password != confirm:
            self.add_error('confirm_password', "Las contraseñas no coinciden.")

        # Validar campos obligatorios SOLO si es bibliotecario
        if role == UserRole.LIBRARIAN:
            if not cleaned.get('escolaridad'):
                self.add_error('escolaridad', 'Requerido para bibliotecarios.')
            if not cleaned.get('numero_empleado'):
                self.add_error('numero_empleado', 'Requerido para bibliotecarios.')
            if not cleaned.get('biblioteca'):
                self.add_error('biblioteca', 'Selecciona la biblioteca del bibliotecario.')

        return cleaned

    def save(self, commit=True):
        instance = super().save(commit=False)
        password = self.cleaned.get('password')
        if password:
            instance.set_password(password)  # Usar set_password para encriptar
        if commit:
            instance.save()
        return instance

class RegistroFiadorForm(forms.Form):
    nombres = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellido_paterno = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    apellido_materno = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    domicilio = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    ocupacion = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    nombre_direccion_trabajo = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    telefono_trabajo = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    codigo_postal = forms.CharField(
        max_length=10, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )