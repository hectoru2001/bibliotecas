from django.contrib import admin
from .models import Fiador

@admin.register(Fiador)
class FiadorAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellido_paterno', 'apellido_materno', 'email', 'telefono', 'biblioteca')
    list_filter = ('biblioteca', 'role', 'responsabilidad')
    search_fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'email', 'telefono')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombres', 'apellido_paterno', 'apellido_materno', 'domicilio', 'codigo_postal')
        }),
        ('Contacto', {
            'fields': ('telefono', 'email')
        }),
        ('Información Laboral', {
            'fields': ('ocupacion', 'nombre_direccion_trabajo', 'telefono_trabajo')
        }),
        ('Configuración', {
            'fields': ('role', 'responsabilidad', 'retraso', 'suspension', 'aviso_usuario')
        }),
        ('Relaciones', {
            'fields': ('biblioteca', 'registro')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )