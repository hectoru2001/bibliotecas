# salas/forms.py
from django import forms
from .models import ReservaSala
from django.utils import timezone
from datetime import datetime, timedelta


class SalaForm(forms.ModelForm):
    class Meta:
        model = ReservaSala
        fields = [
            'apellido_paterno', 'apellido_materno', 'nombre_resp','nombre_institucion',
            'nombre_evento', 'tipo_evento','resena_proyecto','fecha_reserva',
            'telefono', 'edad_rango','biblioteca'
        ]
        
        widgets = {
            'apellido_paterno': forms.TextInput(attrs={'placeholder': 'Apellido Paterno', 'required': 'required'}),
            'apellido_materno': forms.TextInput(attrs={'placeholder': 'Apellido Materno', 'required': 'required'}),
            'nombre_resp': forms.TextInput(attrs={'placeholder': 'Nombre del Responsable', 'required': 'required'}),
            'nombre_institucion': forms.TextInput(attrs={'placeholder': 'Nombre ', 'required': 'required'}),
            'nombre_evento': forms.TextInput(attrs={'placeholder': 'Nombre del evento', 'required': 'required'}),
            'tipo_evento': forms.Select(attrs={'class': 'form-control'}),
            'resena_proyecto': forms.TextInput(attrs={'placeholder': 'Ejemplo: Proyecto de fisica II', 'required': 'required'}),
            'fecha_reserva': forms.DateTimeInput(
                attrs={
                    'type': 'datetime-local',
                    'required': 'required',
                    'min': (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M')
                }
            ),
            'telefono': forms.TextInput(attrs={'placeholder': 'Telefono'}),
            'edad_rango': forms.Select(attrs={'required': 'required'}),
            'biblioteca': forms.Select(attrs={'required': 'required'}),

        }


    def clean_fecha_reserva(self):
        fecha = self.cleaned_data.get('fecha_reserva')
        if fecha:
            fecha_minima = timezone.now() + timedelta(days=7)
            if fecha < fecha_minima:
                raise forms.ValidationError("La fecha de reserva debe ser al menos con 7 dias de anticipacion.")
        return fecha
