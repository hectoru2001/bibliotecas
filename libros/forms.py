from django import forms
from .models import Libro, Categoria, Estado

class LibroForm(forms.ModelForm):
    class Meta:
        model = Libro
        fields = ['numadqui', 'titulo', 'autor', 'isbn', 'editorial', 
                 'año_publicacion', 'categoria', 'descripcion', 'estado', 
                 'portada', 'ubicacion', 'biblioteca', 'disponible']
        exclude = ['user']
        widgets = {
            'numadqui': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'titulo': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'autor': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'isbn': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'editorial': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'año_publicacion': forms.NumberInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'min': 1000, 'max': 2100}),
            'categoria': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'descripcion': forms.Textarea(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm', 'rows': 4}),
            'estado': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'portada': forms.FileInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'ubicacion': forms.TextInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'biblioteca': forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-red-500 focus:border-red-500 sm:text-sm'}),
        }
        labels = {
            'numadqui': 'Numero de Adquisicion',
            'titulo': 'Titulo',
            'autor': 'Autor',
            'isbn': 'ISBN',
            'editorial': 'Editorial',
            'año_publicacion': 'Año de Publicación',
            'categoria': 'Categoría',
            'descripcion': 'Descripción',
            'estado': 'Estado',
            'portada': 'Portada',
            'ubicacion': 'Ubicación en biblioteca',
            'biblioteca': 'Biblioteca',
            'disponible': 'Disponible',
        }