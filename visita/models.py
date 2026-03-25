# visita/models.py
from django.db import models
from django.utils import timezone
from bibliotecas.models import Biblioteca

class VisitaGuiada(models.Model):
    # Definición de rangos de edad
    EDAD_RANGOS = [
        ('menores_12', 'Menores de 12 años'),
        ('13_17', '13 a 17 años'),
        ('18_29', '18 a 29 años'),
        ('30_59', '30 a 59 años'),
        ('mayores_60', 'Mayores de 60 años'),
    ]
    # Definición de horarios
    HORARIOS = [
        ('08_09', '8:00 AM - 09:00 AM'),
        ('09_10', '9:00 AM - 10:00 AM'),
        ('10_11', '10:00 AM - 11:00 AM'),
        ('11_12', '11:00 AM - 12:00 PM'),
        ('12_01', '12:00 AM - 1:00 PM'),
        ('02_03', '2:00 PM - 3:00 PM'),
        ('03_04', '3:00 PM - 4:00 PM'),
        ('04_05', '4:00 PM - 5:00 PM'),
        ('05_06', '5:00 PM - 6:00 PM'),
        ('06_07', '6:00 PM - 7:00 PM'),
        ('07_08', '7:00 PM - 8:00 PM'),
    ]
    nombre_institucion = models.CharField(max_length=255, verbose_name="Nombre de la institución")
    nombre_director = models.CharField(max_length=255, verbose_name="Nombre del director")
    fecha_visita = models.DateField(verbose_name="Fecha de la Visita")
    proposito = models.CharField(max_length=255, verbose_name="Propósito de la Visita")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono de la institución", blank=True, default="")
    edad_rango = models.CharField(
        max_length=20,
        choices=EDAD_RANGOS,
        verbose_name="Rango de Edad",
        null=True,
        blank=True
    )
    total_asistencia = models.IntegerField(null=True, blank=True, verbose_name="Total de Asistencia")
    email = models.EmailField(verbose_name="Correo electrónico institucional",unique=False )
    apellido_paterno = models.CharField(max_length=255, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=255, verbose_name="Apellido Materno")
    nombre_resp = models.CharField(max_length=255, verbose_name="Nombre del Responsable")
    ocupacion = models.CharField(max_length=255, verbose_name="Ocupación", blank=True, default="")
    telefono_resp = models.CharField(max_length=20, verbose_name="Teléfono del Responsable", blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, null=True, blank=True)
    horario = models.CharField(
        max_length=20,
        choices=HORARIOS,
        verbose_name="Horario de Llegada",
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Visita'
        verbose_name_plural = 'Visitas'

    def __str__(self):
        return f"Visita de {self.nombre_institucion} a {self.biblioteca.nombre} el {self.fecha_visita}"