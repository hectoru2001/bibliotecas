from django.contrib import admin
from .models import Biblioteca

@admin.register(Biblioteca)
class BibliotecaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'nombre_corto', 'director', 'telefono', 'email', 'opening_time', 'closing_time', 'role')
    list_filter = ('role', 'created_at')
    search_fields = ('nombre', 'nombre_corto', 'director', 'email')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('nombre', 'nombre_corto', 'num_coleccion', 'director')
        }),
        ('Información de contacto', {
            'fields': ('direccion', 'telefono', 'email', 'ubicacion')
        }),
        ('Horarios', {
            'fields': ('opening_time', 'closing_time'),
            'description': 'Horario de operación de la biblioteca (formato 24 horas)'
        }),
        ('Detalles adicionales', {
            'fields': ('reseña', 'role', 'foto')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )