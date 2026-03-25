from django import forms
from libros.models import Libro, Estado
from .models import Prestamo

class ReservaForm(forms.Form):
    libro_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        if not self.user or not self.user.is_authenticated:
            raise forms.ValidationError("Debes estar autenticado para reservar un libro.")
        
        libro_id = cleaned_data.get('libro_id')
        if not libro_id:
            raise forms.ValidationError("No se proporcionó un libro para reservar.")
        
        try:
            libro = Libro.objects.get(id=libro_id)
            if libro.estado not in [Estado.AVAILABLE, Estado.RESERVED]:
                raise forms.ValidationError("El libro no está disponible para reservar.")
            if libro.biblioteca != self.user.biblioteca:
                raise forms.ValidationError("No tienes credencial válida para la biblioteca del libro.")
            cleaned_data['libro'] = libro
        except Libro.DoesNotExist:
            raise forms.ValidationError("El libro seleccionado no existe.")
        
        return cleaned_data

    def save(self):
        libro = self.cleaned_data['libro']
        prestamo = Prestamo(
            usuario=self.user,
            libro=libro,
            biblioteca=libro.biblioteca,
            no_credencial=self.user.no_credencial,
            estado='reservado'
        )
        prestamo.save()
        return prestamo