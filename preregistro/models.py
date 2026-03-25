from django.db import models
from django.utils import timezone
from bibliotecas.models import Biblioteca

class PreRegistro(models.Model):
    apellido_paterno = models.CharField(max_length=255, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=255, verbose_name="Apellido Materno")
    nombres = models.CharField(max_length=255, verbose_name="Nombres")
    fecha_nacimiento = models.DateField(verbose_name="Fecha de Nacimiento")  # Requerido
    sexo = models.CharField(max_length=1, choices=(('H', 'Hombre'), ('M', 'Mujer')), verbose_name="Sexo")  # Requerido
    curp = models.CharField(max_length=18, unique=True, blank=False, null=False)
    domicilio = models.CharField(max_length=255, verbose_name="Domicilio", blank=True, default="")
    codigo_postal = models.CharField(max_length=10, verbose_name="Código Postal", blank=True, default="")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono", blank=True, default="")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    username = models.CharField(max_length=255, unique=True, verbose_name="Nombre de usuario")
    ocupacion = models.CharField(max_length=255, verbose_name="Ocupación", blank=True, default="")
    escuela_trabajo = models.CharField(max_length=255, verbose_name="Escuela o trabajo", blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Preregistro'
        verbose_name_plural = 'Preregistros'

    def __str__(self):
        return self.username