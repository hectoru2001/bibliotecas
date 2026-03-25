from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from django.core.exceptions import ValidationError

from .models import Registro, UserRole


class RegistroAdminForm(forms.ModelForm):
    """
    Se usa en el change form (edición) para validar requeridos cuando role=librarian.
    En el add form también validaremos en save_model para cubrir ambos caminos.
    """
    class Meta:
        model = Registro
        fields = "__all__"

    def clean(self):
        cleaned = super().clean()
        role = cleaned.get("role")
        if role == UserRole.LIBRARIAN:
            required = ["biblioteca", "edad", "escolaridad", "numero_empleado"]
            errors = {f: "Este campo es obligatorio para bibliotecarios." 
                      for f in required if not cleaned.get(f)}
            if errors:
                raise ValidationError(errors)

            # Unicidad opcional de número de empleado entre bibliotecarios
            num = cleaned.get("numero_empleado")
            if num:
                qs = Registro.objects.filter(role=UserRole.LIBRARIAN, numero_empleado=num)
                if self.instance.pk:
                    qs = qs.exclude(pk=self.instance.pk)
                if qs.exists():
                    self.add_error("numero_empleado", "Ya existe un bibliotecario con este número de empleado.")
        return cleaned


@admin.register(Registro)
class RegistroAdmin(UserAdmin):
    form = RegistroAdminForm   # para edición; el alta también la cubrimos con save_model

    # Qué ves en el listado
    list_display = (
        'email', 'username', 'get_full_name', 'biblioteca',
        'role', 'escolaridad', 'numero_empleado', 'is_staff'
    )
    list_filter = ('biblioteca', 'role', 'escolaridad', 'is_staff', 'is_superuser', 'created_at')
    search_fields = (
        'email', 'username', 'nombres', 'apellido_paterno', 'apellido_materno',
        'numero_empleado'
    )
    readonly_fields = ('created_at', 'updated_at', 'no_credencial')  # muestra el consecutivo

    ordering = ('email',)

    # Edición (change form)
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Información Personal', {
            'fields': (
                'nombres', 'apellido_paterno', 'apellido_materno',
                'edad', 'escolaridad', 'domicilio', 'codigo_postal', 'telefono'
            )
        }),
        ('Información Profesional', {
            'fields': ('ocupacion', 'escuela_trabajo', 'telefono_escuela_trabajo')
        }),
        ('Relaciones', {'fields': ('biblioteca', 'no_credencial')}),
        ('Configuración', {'fields': ('role', 'numero_empleado', 'fecha_vencimiento')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser')}),
        ('Fechas Importantes', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    # Alta (add form)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        ('Información Personal', {
            'fields': (
                'nombres', 'apellido_paterno', 'apellido_materno',
                'edad', 'escolaridad', 'domicilio', 'codigo_postal', 'telefono'
            )
        }),
        ('Información Profesional', {'fields': ('ocupacion', 'escuela_trabajo', 'telefono_escuela_trabajo')}),
        ('Relaciones', {'fields': ('biblioteca',)}),
        ('Configuración', {'fields': ('role', 'numero_empleado', 'fecha_vencimiento')}),
    )

    class Media:
        # Muestra/oculta campos según el rol en el admin
        js = ('registros/js/registro_toggle.js',)

    def save_model(self, request, obj, form, change):
        """
        Validación de requeridos también en el add form (cuando UserAdmin usa su add_form),
        y como “cinturón y tirantes” para cualquier guardado.
        """
        if obj.role == UserRole.LIBRARIAN:
            missing = []
            if not obj.biblioteca:        missing.append('biblioteca')
            if not obj.edad:              missing.append('edad')
            if not obj.escolaridad:       missing.append('escolaridad')
            if not obj.numero_empleado:   missing.append('numero_empleado')
            if missing:
                raise ValidationError({f: "Este campo es obligatorio para bibliotecarios." for f in missing})

            # Unicidad de número de empleado entre bibliotecarios
            if obj.numero_empleado:
                qs = Registro.objects.filter(role=UserRole.LIBRARIAN, numero_empleado=obj.numero_empleado)
                if obj.pk:
                    qs = qs.exclude(pk=obj.pk)
                if qs.exists():
                    raise ValidationError({"numero_empleado": "Ya existe un bibliotecario con este número de empleado."})

        super().save_model(request, obj, form, change)
