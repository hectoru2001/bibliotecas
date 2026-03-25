from django.db import models
from bibliotecas.models import Biblioteca
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from fichas.models import Ficha

class UserRole(models.TextChoices):
    ADMIN = 'admin', 'Admin'
    LIBRARIAN = 'librarian', 'Bibliotecario'
    VISITOR = 'visitor', 'Visitante'

class Categoria(models.TextChoices):
    FICTION = 'fiction', 'Ficción'
    NONFICTION = 'nonfiction', 'No Ficción'
    POETRY = 'poetry', 'Poesía'
    SCIENCE = 'science', 'Ciencia'
    LITERATURE = 'literature', 'Literario'
    HISTORY = 'history', 'Historia'
    BIOGRAPHY = 'biography', 'Biografía'
    CHILDREN = 'children', 'Infantil'
    OTHER = 'other', 'Otro'

class Estado(models.TextChoices):
    AVAILABLE = 'available', 'Disponible'
    LOANED = 'loaned', 'Prestado'
    RESERVED = 'reserved', 'Reservado'
    REPAIR = 'repair', 'En Reparacion'
    LOST = 'lost', 'Extraviado'

class Libro(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                  null=True, related_name='libros_creados')
    numadqui = models.OneToOneField(Ficha, on_delete=models.CASCADE, related_name='libro', to_field='ficha_no')
    titulo = models.CharField(max_length=255, verbose_name="Título")
    autor = models.CharField(max_length=255, verbose_name="Autor")
    isbn = models.CharField(max_length=20, verbose_name="ISBN", blank=True, null=True)
    editorial = models.CharField(max_length=255, verbose_name="Editorial", blank=True, null=True)
    año_publicacion = models.IntegerField(null=True, blank=True)
    categoria = models.CharField(max_length=50, choices=Categoria.choices, default=Categoria.FICTION)
    descripcion = models.TextField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=Estado.choices, default=Estado.AVAILABLE)
    portada = models.ImageField(upload_to='portadas', null=True, blank=True, verbose_name="Portada")
    ubicacion = models.CharField(max_length=100, verbose_name="Ubicación en biblioteca", blank=True)
    role = models.CharField(max_length=50, choices=UserRole.choices)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, related_name='libros')
    # Campos de estadísticas
    disponible = models.BooleanField(default=True)
    prestamos = models.IntegerField(default=0)
    reservas = models.IntegerField(default=0)
    devoluciones = models.IntegerField(default=0)
    busquedas = models.IntegerField(default=0)
    vistas = models.IntegerField(default=0)
    descargas = models.IntegerField(default=0)
    lecturas = models.IntegerField(default=0)
    favoritos = models.IntegerField(default=0)
    valoraciones = models.IntegerField(default=0)
    comentarios = models.IntegerField(default=0)
    reseñas = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    shares = models.IntegerField(default=0)
    impresiones = models.IntegerField(default=0)
    clicks = models.IntegerField(default=0)
    conversiones = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.titulo} - {self.autor}"
    
    def get_prestamo_reservado(self):
        """Devuelve el primer préstamo con estado 'reservado' asociado al libro, si existe."""
        return self.prestamo_set.filter(estado='reservado').first()

    class Meta:
            verbose_name = "Libro"
            verbose_name_plural = "Libros"
            ordering = ['titulo', 'autor']
            indexes = [
                models.Index(fields=['titulo']),
                models.Index(fields=['autor']),
                models.Index(fields=['isbn']),
                models.Index(fields=['estado']),
            ]