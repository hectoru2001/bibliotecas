from django import forms
from .models import Biblioteca

class BibliotecaForm(forms.ModelForm):
    class Meta:
        model = Biblioteca
        fields = [
            'nombre', 'nombre_corto', 'num_coleccion', 'direccion', 'director', 'telefono',
            'email', 'ubicacion', 'reseña', 'role', 'foto',
            'opening_time', 'closing_time',  # ⬅️ nuevos
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'nombre_corto': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'num_coleccion': forms.NumberInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'direccion': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'director': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'telefono': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'email': forms.EmailInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'ubicacion': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),
            'reseña': forms.Textarea(attrs={'rows': 3, 'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'role': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'}),


            'opening_time': forms.TimeInput(format="%H:%M", attrs={
                'type': 'time',
                'step': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'
            }),
            'closing_time': forms.TimeInput(format="%H:%M", attrs={
                'type': 'time',
                'step': '60',
                'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm custom-input-height'
            }),
        }
        labels = {
            'nombre': 'Nombre de la biblioteca',
            'nombre_corto': 'Nombre corto',
            'num_coleccion': 'Número de colección',
            'direccion': 'Dirección',
            'director': 'Director',
            'telefono': 'Teléfono',
            'email': 'Correo electrónico',
            'ubicacion': 'Ubicación',
            'reseña': 'Reseña',
            'role': 'Rol',
            'foto': 'Fotografía',
            'opening_time': 'Hora de apertura',
            'closing_time': 'Hora de cierre',
        }

    def clean(self):
        cleaned = super().clean()
        opening = cleaned.get('opening_time')
        closing = cleaned.get('closing_time')
        if opening and closing and opening >= closing:
            self.add_error('closing_time', 'La hora de cierre debe ser mayor que la de apertura.')
        return cleaned
