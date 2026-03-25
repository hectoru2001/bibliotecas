from django.db import models
from bibliotecas.models import Biblioteca
from django.conf import settings

class Bibliotecario(models.Model):
    user = models.OneToOneField('registros.Registro', on_delete=models.CASCADE, related_name='bibliotecario', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, 
                                  related_name='bibliotecarios_creados')
    nombre = models.CharField(max_length=255, verbose_name="Nombre")
    apellido = models.CharField(max_length=255, verbose_name="Apellido")
    email = models.EmailField(verbose_name="Correo electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.CharField(max_length=255, verbose_name="Dirección")
    active = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.biblioteca.nombre}"

    def save(self, *args, **kwargs):
        if self.user:
            self.email = self.user.email
            if self.user.role == 'librarian' and not self.user.is_staff:
                self.user.is_staff = True
                self.user.save()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Bibliotecario"
        verbose_name_plural = "Bibliotecarios"
        ordering = ['apellido', 'nombre']