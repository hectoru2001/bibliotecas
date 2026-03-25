from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from django import forms
from registros.models import Registro
from bibliotecas.models import Biblioteca
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    # AÃ±adir email como campo requerido
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Incluir email en campos
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('El correo electrÃ³nico es obligatorio')
        
        # Comprobar si hay algÃºn usuario con este email (excepto el usuario actual en caso de ediciÃ³n)
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrÃ³nico ya estÃ¡ en uso')
        
        return email

class UserAdminForm(forms.ModelForm):
    password = forms.CharField(
        label="ContraseÃ±a",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text="Deja este campo en blanco para mantener la contraseÃ±a actual"
    )
    
    confirm_password = forms.CharField(
        label="Confirmar contraseÃ±a",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False
    )
    
    biblioteca = forms.ModelChoiceField(
        queryset=Biblioteca.objects.all(),
        required=True,
        label='Biblioteca',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Agregar estos campos como campos adicionales del formulario
    is_active = forms.BooleanField(
        required=False, 
        label="Usuario activo",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    is_staff = forms.BooleanField(
        required=False, 
        label="Staff",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    is_superuser = forms.BooleanField(
        required=False, 
        label="Superusuario",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Registro
        fields = [
            'nombres', 'apellido_paterno', 'apellido_materno',
            'domicilio', 'codigo_postal', 'telefono', 'email', 'username',
            'ocupacion', 'escuela_trabajo', 'telefono_escuela_trabajo',
            'role', 'biblioteca'

        ]
        widgets = {
            # Los widgets se mantienen igual
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Si es modo ediciÃ³n, obtener valores de User
        if self.instance and self.instance.pk:
            self.fields['password'].help_text = "Deja este campo en blanco para mantener la contraseÃ±a actual"
            self.fields['biblioteca'].initial = self.instance.biblioteca
            
            # Inicializar campos de User si el modelo Registro estÃ¡ relacionado con User
            if hasattr(self.instance, 'user'):  # Si Registro tiene relaciÃ³n con User
                self.fields['is_active'].initial = self.instance.user.is_active
                self.fields['is_staff'].initial = self.instance.user.is_staff
                self.fields['is_superuser'].initial = self.instance.user.is_superuser
        
        # Marcar campos obligatorios
        for field_name in ['nombres', 'apellido_paterno', 'email', 'username']:
            self.fields[field_name].required = True
    
    def save(self, commit=True):
        registro = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        # Si hay usuario asociado (esto depende de tu modelo)
        if hasattr(registro, 'user'):
            user = registro.user
            if password:
                user.set_password(password)
                
            # Actualizar campos de User
            user.is_active = self.cleaned_data.get('is_active', False)
            user.is_staff = self.cleaned_data.get('is_staff', False)
            user.is_superuser = self.cleaned_data.get('is_superuser', False)
            
            if commit:
                user.save()
        
        if commit:
            registro.save()
            
        return registro