from django.db import models

class Ficha(models.Model):
    ficha_no = models.IntegerField(primary_key=True)  # Primary Key, Not NULL
    fecha = models.DateTimeField(null=True, blank=True)  # timestamp without time zone
    fechamod = models.DateTimeField(null=True, blank=True)  # timestamp without time zone
    datosfijos = models.CharField(max_length=60, null=True, blank=True)  # character varying(60)
    etiquetasmar = models.TextField(null=True, blank=True)  # text
    tipomaterial = models.SmallIntegerField(default=0)  # smallint, default 0
    isbn = models.CharField(max_length=20, null=True, blank=True)  # character varying(20)
    titulo = models.CharField(max_length=50, null=True, blank=True)  # character varying(50)
    autor = models.CharField(max_length=50, null=True, blank=True)  # character varying(50)
    clasificacion = models.CharField(max_length=50, null=True, blank=True)  # character varying(50)

    class Meta:
        db_table = 'fichas'  # Nombre de la tabla en la base de datos

    def __str__(self):
        return f"Ficha {self.ficha_no} - {self.titulo}"

class ImportacionFicha(models.Model):

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('procesando', 'Procesando'),
        ('terminado', 'Terminado'),
        ('error', 'Error'),
    ]

    archivo = models.FileField(upload_to="imports/")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')

    progreso = models.IntegerField(default=0)  # %
    total = models.IntegerField(default=0)
    procesados = models.IntegerField(default=0)

    error = models.TextField(null=True, blank=True)

    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Importación #{self.id} - {self.estado}"