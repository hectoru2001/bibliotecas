from django.db import models
from datetime import datetime
from django.utils import timezone
from datetime import datetime

class AgendaBiblioAprende(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField()
    hora = models.TimeField()
    fecha_fin = models.DateField(verbose_name="Fecha de finalizacion", null=True, blank=True)
    hora_fin = models.TimeField(verbose_name="Horario de finalizacion", null=True, blank=True)
    biblioteca = models.ForeignKey('bibliotecas.Biblioteca', on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='eventos/biblioaprende/')

    def __str__(self):
        return self.nombre
    

    def ya_finalizo(self):
        if self.fecha_fin and self.hora_fin:
            fin = datetime.combine(self.fecha_fin, self.hora_fin)
            # compara con ahora "naive" local o convierte:
            ahora = timezone.localtime().replace(tzinfo=None)
            return ahora > fin
        return False


class AgendaCultural(models.Model):
    nombre = models.CharField(max_length=200)
    lugar = models.CharField(max_length=255)
    fecha = models.DateField()
    enlace = models.URLField()
    imagen = models.ImageField(upload_to='eventos/cultural/')

    def __str__(self):
        return self.nombre

