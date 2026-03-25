from django.contrib import admin
from .models import Bibliotecario

@admin.register(Bibliotecario)
class BibliotecarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido', 'email', 'biblioteca','active')
    list_filter = ('active', 'biblioteca')
    search_fields = ('nombre', 'apellido', 'email')
    readonly_fields = ('fecha_creacion', 'fecha_actualizacion')
    fieldsets = (
        (None, {
            'fields': ('user', 'nombre', 'apellido')
        }),
        ('Información de contacto', {
            'fields': ('email', 'telefono', 'direccion')
        }),
        ('Configuración', {
            'fields': ('biblioteca', 'active')
        }),
        ('Fechas', {
            'fields': ('fecha_creacion', 'fecha_actualizacion'),
            'classes': ('collapse',)
        }),
    )