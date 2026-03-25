from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
from bibliotecas.models import Biblioteca
from libros.models import Libro, Estado  # AsegÃºrate de importar Estado

class Prestamo(models.Model):
    ESTADO_CHOICES = (
        ('reservado', 'Reservado'),
        ('prestado', 'Prestado'),
        ('devuelto', 'Devuelto'),
    )

    usuario = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, verbose_name="Usuario")
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE, verbose_name="Libro")
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, verbose_name="Biblioteca")
    no_credencial = models.IntegerField(verbose_name="No. Credencial", null=True, blank=True)
    fecha_reserva = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de reserva")
    fecha_prestamo = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de prÃ©stamo")
    fecha_devolucion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de devoluciÃ³n")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='reservado', verbose_name="Estado")

    def clean(self):
        if self.libro.biblioteca != self.usuario.biblioteca:
            raise ValidationError("El usuario no tiene credencial vÃ¡lida para la biblioteca del libro.")
        # Usa Estado directamente, no Libro.Estado
        if self.estado == 'reservado' and self.libro.estado not in [Estado.AVAILABLE, Estado.RESERVED]:
            raise ValidationError("El libro no estÃ¡ disponible para reservar.")
        if self.estado == 'prestado' and self.libro.estado == Estado.LOANED:
            raise ValidationError("El libro ya estÃ¡ prestado.")
        if self.no_credencial and self.no_credencial != self.usuario.no_credencial:
            raise ValidationError("El nÃºmero de credencial no coincide con el del usuario.")

    def save(self, *args, **kwargs):
        if not self.no_credencial:
            self.no_credencial = self.usuario.no_credencial

        self.full_clean()

        # Usa Estado directamente, no Libro.Estado
        if self.estado == 'reservado' and self.libro.estado == Estado.AVAILABLE:
            self.libro.estado = Estado.RESERVED
            self.libro.reservas += 1
            self.libro.disponible = False
        elif self.estado == 'prestado' and self.libro.estado in [Estado.AVAILABLE, Estado.RESERVED]:
            self.libro.estado = Estado.LOANED
            self.libro.prestamos += 1
            self.libro.disponible = False
            self.fecha_prestamo = self.fecha_prestamo or timezone.now()
        elif self.estado == 'devuelto':
            self.libro.estado = Estado.AVAILABLE
            self.libro.devoluciones += 1
            self.libro.disponible = True
            self.fecha_devolucion = self.fecha_devolucion or timezone.now()

        self.libro.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.libro.titulo} ({self.estado})"

    class Meta:
        verbose_name = "PrÃ©stamo"
        verbose_name_plural = "PrÃ©stamos"