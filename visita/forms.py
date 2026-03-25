from django import forms
from django.utils import timezone
from datetime import timedelta
from .models import VisitaGuiada

class VisitaForm(forms.ModelForm):
    # Ahora es DateField porque el modelo tiene DateField
    fecha_visita = forms.DateField(
        input_formats=['%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'required': 'required',
                # el min se setea en __init__
            }
        )
    )

    class Meta:
        model = VisitaGuiada
        fields = [
            'nombre_institucion', 'nombre_director', 'fecha_visita', 'proposito',
            'telefono', 'edad_rango', 'total_asistencia', 'email', 'apellido_paterno',
            'apellido_materno', 'nombre_resp', 'ocupacion', 'telefono_resp', 'biblioteca',
            'horario'
        ]
        widgets = {
            'nombre_institucion': forms.TextInput(attrs={'placeholder': 'Nombre de la institución', 'required': 'required'}),
            'nombre_director': forms.TextInput(attrs={'placeholder': 'Nombre del director', 'required': 'required'}),
            'proposito': forms.TextInput(attrs={'placeholder': 'Ejemplo: Visita guiada', 'required': 'required'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de la institución'}),
            'edad_rango': forms.Select(attrs={'required': 'required'}),
            'total_asistencia': forms.NumberInput(attrs={'placeholder': 'Total de asistentes', 'required': 'required'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo electrónico institucional', 'required': 'required'}),
            'apellido_paterno': forms.TextInput(attrs={'placeholder': 'Apellido Paterno', 'required': 'required'}),
            'apellido_materno': forms.TextInput(attrs={'placeholder': 'Apellido Materno', 'required': 'required'}),
            'nombre_resp': forms.TextInput(attrs={'placeholder': 'Nombre del Responsable', 'required': 'required'}),
            'ocupacion': forms.TextInput(attrs={'placeholder': 'Ocupación'}),
            'telefono_resp': forms.TextInput(attrs={'placeholder': 'Teléfono del Responsable'}),
            'biblioteca': forms.Select(attrs={'required': 'required'}),
            'horario': forms.Select(attrs={'required': 'required'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # min dinámico: hoy + 7 días en formato YYYY-MM-DD
        self.fields['fecha_visita'].widget.attrs['min'] = (
            (timezone.localdate() + timedelta(days=7)).strftime('%Y-%m-%d')
        )

    def clean_fecha_visita(self):
        fecha = self.cleaned_data.get('fecha_visita')  # date
        if fecha:
            fecha_minima = timezone.localdate() + timedelta(days=7)
            if fecha < fecha_minima:
                raise forms.ValidationError(
                    "La fecha de la visita debe ser al menos con 7 días de anticipación."
                )
        return fecha
