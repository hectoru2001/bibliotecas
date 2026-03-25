# projects/bibliotecarios/forms.py
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Bibliotecario
from bibliotecas.models import Biblioteca

User = get_user_model()

class BibliotecarioForm(forms.ModelForm):
    class Meta:
        model = Bibliotecario
        fields = ['nombre', 'apellido', 'email', 'telefono', 'direccion', 'active', 'biblioteca']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'apellido': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'telefono': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'direccion': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'active': forms.CheckboxInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'biblioteca': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
        }
        labels = {
            'nombre': 'Nombre del bibliotecario',
            'apellido': 'Apellidos',
            'email': 'Correo electrónico',
            'telefono': 'Teléfono',
            'direccion': 'Dirección',
            'active': 'Activo',
            'biblioteca': 'Biblioteca',
        }

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('request_user', None)
        super().__init__(*args, **kwargs)

        # Limitar bibliotecas (no-superusuarios)
        if self.request_user and not self.request_user.is_superuser:
            bprof = getattr(self.request_user, 'bibliotecario', None)
            if bprof and bprof.biblioteca_id:
                self.fields['biblioteca'].queryset = Biblioteca.objects.filter(id=bprof.biblioteca_id)

        # UX: si no tiene permiso de cambio, deshabilita 'active'
        if self.request_user and not self.request_user.has_perm('bibliotecarios.change_bibliotecario'):
            self.fields['active'].disabled = True

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip().lower()
        qs = Bibliotecario.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError('Ya existe un bibliotecario con ese correo.')
        return email

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Autolink al Registro por email (si existe)
        if not instance.user:
            user = User.objects.filter(email__iexact=instance.email).order_by('id').first()
            if user:
                instance.user = user

        if commit:
            instance.save()
        return instance
