
from django.db import models
from django.utils import timezone
from bibliotecas.models import Biblioteca

class ReservaSala(models.Model):

    TIPO_EVENTO_CHOICES = [
        ('reunion', 'Reunion'),
        ('curso', 'Curso'),
        ('exhibicion', 'Exhibicion'),
        ('colaborativo', 'Trabajo colaborativo'),
    ]

    EDAD_RANGOS = [
        ('menores_12', 'Menores de 12 '),
        ('13_17', '13 a 17 '),
        ('18_29', '18 a 29 '),
        ('30_59', '30 a 59 '),
        ('mayores_60', 'Mayores de 60 '),
    ]

    apellido_paterno = models.CharField(max_length=255, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=255, verbose_name="Apellido Materno")
    nombre_resp = models.CharField(max_length=255, verbose_name="Nombre del Responsable")
    nombre_institucion = models.CharField(max_length=255, verbose_name="Nombre de la institucion")
    nombre_evento = models.CharField(max_length=255, verbose_name="Nombre del evento")
    tipo_evento = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES, verbose_name="Tipo de evento")
    resena_proyecto = models.TextField(null=True, blank=True)
    fecha_reserva = models.DateTimeField(verbose_name="Fecha de la Reserva")
    telefono = models.CharField(max_length=20, verbose_name="Telefono", blank=True, default="")
    edad_rango = models.CharField(
        max_length=20,
        choices=EDAD_RANGOS,
        verbose_name="Rango de Edad",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'
    def __str__(self):
        return f"Rserva de {self.nombre_resp} a {self.biblioteca.nombre} el {self.fecha_reserva}"