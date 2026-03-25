from django.db import models
from bibliotecas.models import Biblioteca

class UserRole(models.TextChoices):
    VISITOR = 'visitor', 'Visitante'

class Fiador(models.Model):

    registro = models.OneToOneField('registros.Registro', on_delete=models.CASCADE, related_name='fiador')
    apellido_paterno = models.CharField(max_length=255, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=255, verbose_name="Apellido Materno")
    nombres = models.CharField(max_length=255, verbose_name="Nombres")
    domicilio = models.CharField(max_length=255, verbose_name="Domicilio")  
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    email = models.EmailField(verbose_name="Correo electrónico")
    ocupacion = models.CharField(max_length=255, verbose_name="Ocupación")
    nombre_direccion_trabajo = models.CharField(max_length=255, verbose_name="Nombre de la dirección de trabajo")
    telefono_trabajo = models.CharField(max_length=20, verbose_name="Teléfono de trabajo")
    role = models.CharField(max_length=50, choices=UserRole.choices)
    responsabilidad = models.BooleanField()
    retraso = models.CharField(max_length=255)
    suspension = models.CharField(max_length=255)
    aviso_usuario = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

