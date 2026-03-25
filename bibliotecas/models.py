from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    LIBRARIAN = 'librarian', 'Bibliotecario'
    VISITOR = 'visitor', 'Visitante'

class Biblioteca(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255, verbose_name="Nombre de la biblioteca")
    nombre_corto = models.CharField(max_length=50, verbose_name="Nombre corto", null=True, blank=True)
    num_coleccion = models.IntegerField(null=True, blank=True, verbose_name="Numero de coleccion")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    director = models.CharField(max_length=255, verbose_name="Director")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    ubicacion = models.CharField(max_length=255,)
    reseña = models.TextField(verbose_name="Reseña")
    role = models.CharField(max_length=50, choices=UserRole.choices)
    foto = models.ImageField(upload_to="bibliotecas", null=True, blank=True, verbose_name="Fotografía")
    opening_time = models.TimeField(verbose_name="Hora de apertura")
    closing_time = models.TimeField(verbose_name="Hora de cierre")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    def clean(self):
        super().clean()
        if self.opening_time and self.closing_time and self.opening_time >= self.closing_time:
            # Nota: si quisieras permitir horarios que cruzan medianoche, cambia esta validación.
            raise ValidationError({
                "closing_time": _("La hora de cierre debe ser mayor que la de apertura.")
            })

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = "Biblioteca"
        verbose_name_plural = "Bibliotecas"
