from django.contrib import admin
from .models import Libro

@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    # Eliminar 'disponible' y 'biblioteca' que no existen en el modelo
    list_display = ('titulo', 'autor', 'isbn', 'categoria')
    list_filter = ('role',)
    search_fields = ('titulo', 'autor', 'isbn', 'numadqui')
    readonly_fields = ('fecha_creacion',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('user', 'numadqui', 'titulo', 'autor', 'isbn', 'categoria')
        }),
        ('Detalles adicionales', {
            'fields': ('editor', 'año_publicacion', 'descripcion', 'estado')
        }),
        ('Portada', {
            'fields': ('portada',)
        }),
        ('Configuración', {
            'fields': ('role',)
        }),
        ('Fechas', {
            'fields': ('fecha_creacion',),
            'classes': ('collapse',)
        }),
    )