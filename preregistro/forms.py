from django import forms
from .models import PreRegistro
from bibliotecas.models import Biblioteca
import re
from datetime import datetime

class PreRegistroForm(forms.ModelForm):


    class Meta:
        model = PreRegistro
        fields = [
            'apellido_paterno', 'apellido_materno', 'nombres', 'fecha_nacimiento',
            'sexo', 'curp', 'domicilio', 'codigo_postal', 'telefono', 'email',
            'username', 'ocupacion', 'escuela_trabajo', 'biblioteca'
        ]
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'placeholder': 'Apellido Paterno', 'required': 'required'}),
            'apellido_materno': forms.TextInput(attrs={'placeholder': 'Apellido Materno', 'required': 'required'}),
            'nombres': forms.TextInput(attrs={'placeholder': 'Nombres', 'required': 'required'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'required': 'required'}),
            'sexo': forms.Select(attrs={'required': 'required', 'class': 'form-control'}),
            'curp': forms.TextInput(attrs={'placeholder': 'CURP', 'class': 'form-control'}),
            'domicilio': forms.TextInput(attrs={'placeholder': 'Domicilio', 'required': 'required'}),
            'codigo_postal': forms.TextInput(attrs={'placeholder': 'Código Postal', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico', 'required': 'required'}),
            'username': forms.TextInput(attrs={'placeholder': 'Nombre de usuario', 'required': 'required'}),
            'ocupacion': forms.TextInput(attrs={'placeholder': 'Ocupación', 'required': 'required'}),
            'escuela_trabajo': forms.TextInput(attrs={'placeholder': 'Escuela o trabajo', 'required': 'required'}),
            'biblioteca': forms.Select(attrs={'required': 'required', 'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_nacimiento = cleaned_data.get('fecha_nacimiento')
        sexo = cleaned_data.get('sexo')

        if not fecha_nacimiento:
            self.add_error('fecha_nacimiento', 'Este campo es obligatorio.')
        if not sexo:
            self.add_error('sexo', 'Este campo es obligatorio.')

        return cleaned_data

    def clean_curp(self):
        curp = self.cleaned_data.get('curp')
        if curp:
            curp = curp.upper()
            curp_regex = r'^[A-Z]{4}\d{6}[HM][A-Z]{5}[0-9A-Z][0-9]$'
            if not re.match(curp_regex, curp):
                raise forms.ValidationError("El CURP no tiene un formato válido.")
        return curp

