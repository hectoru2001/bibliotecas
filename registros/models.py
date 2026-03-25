# registros/models.py
from datetime import date, timedelta

from django.db import models
from django.db.models import Q
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin,
    Permission, Group
)
from django.contrib.contenttypes.models import ContentType

from bibliotecas.models import Biblioteca


def get_fecha_vencimiento_default():
    return date.today() + timedelta(days=365 * 2)


class UserRole(models.TextChoices):
    VISITOR = "visitor", "Visitante"
    LIBRARIAN = "librarian", "Bibliotecario"


class RegistroManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("El email es obligatorio")
        if not username:
            raise ValueError("El nombre de usuario es obligatorio")

        extra_fields.setdefault("fecha_vencimiento", get_fecha_vencimiento_default())
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, username, password, **extra_fields)


class Registro(AbstractBaseUser, PermissionsMixin):
    # --- Datos base ---
    fecha_vencimiento = models.DateField(default=get_fecha_vencimiento_default)
    apellido_paterno = models.CharField(max_length=255, verbose_name="Apellido Paterno")
    apellido_materno = models.CharField(max_length=255, verbose_name="Apellido Materno")
    nombres = models.CharField(max_length=255, verbose_name="Nombres")

    edad = models.IntegerField(null=True, blank=True)
    curp = models.CharField(max_length=18, unique=True, blank=True, null=True)
    domicilio = models.CharField(max_length=255, blank=True, default="", verbose_name="Domicilio")
    codigo_postal = models.CharField(max_length=10, blank=True, default="", verbose_name="Código Postal")
    telefono = models.CharField(max_length=20, blank=True, default="", verbose_name="Teléfono")
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    username = models.CharField(max_length=255, unique=True, verbose_name="Nombre de usuario")
    ocupacion = models.CharField(max_length=255, blank=True, default="", verbose_name="Ocupación")
    escuela_trabajo = models.CharField(max_length=255, blank=True, default="", verbose_name="Escuela o trabajo")
    telefono_escuela_trabajo = models.CharField(max_length=20, blank=True, default="", verbose_name="Teléfono de la escuela o trabajo")
    role = models.CharField(max_length=50, choices=UserRole.choices, default=UserRole.VISITOR)

    # Relaciones
    biblioteca = models.ForeignKey(Biblioteca, on_delete=models.CASCADE, null=True, blank=True)
    no_credencial = models.IntegerField(verbose_name="No. Credencial", null=True, blank=True)

    # --- Campos solo para bibliotecarios ---
    ESCOLARIDAD_CHOICES = [
        ("primaria", "Primaria"),
        ("secundaria", "Secundaria"),
        ("preparatoria", "Preparatoria"),
        ("tecnico", "Técnico"),
        ("licenciatura", "Licenciatura"),
        ("posgrado", "Posgrado"),
        ("otra", "Otra"),
    ]
    escolaridad = models.CharField(
        max_length=30, choices=ESCOLARIDAD_CHOICES, null=True, blank=True, verbose_name="Escolaridad"
    )
    numero_empleado = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Número de empleado"
    )

    # flags
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # metadatos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "nombres", "apellido_paterno", "apellido_materno"]

    objects = RegistroManager()

    class Meta:
        constraints = [
            # No. credencial único por biblioteca
            models.UniqueConstraint(
                fields=["biblioteca", "no_credencial"],
                name="unique_no_credencial_per_biblioteca",
            ),
            # numero_empleado único SOLO para role = librarian
            models.UniqueConstraint(
                fields=["numero_empleado"],
                condition=Q(role=UserRole.LIBRARIAN),
                name="unique_numero_empleado_librarian",
            ),
        ]

    # ---------- helpers ----------
    def generate_no_credencial(self):
        if not self.biblioteca:
            raise ValueError("Se requiere una biblioteca para generar el número de credencial")
        last = (
            Registro.objects.filter(biblioteca=self.biblioteca)
            .aggregate(models.Max("no_credencial"))["no_credencial__max"]
        )
        self.no_credencial = (last or 0) + 1

    def get_full_name(self):
        return f"{self.nombres} {self.apellido_paterno} {self.apellido_materno}"

    def get_short_name(self):
        return self.nombres

    def __str__(self):
        return self.get_full_name()

    # ---------- política de rol (grupos/permisos) ----------
    def apply_role_policy(self):
        """
        Ajusta is_staff y asigna grupos/permisos según role.
        Se llama DESPUÉS de super().save() (ya hay pk).
        """
        if not self.pk:
            return

        # 1) is_staff coherente con el rol (librarian => staff)
        should_be_staff = self.is_superuser or (self.role == UserRole.LIBRARIAN)
        if self.is_staff != should_be_staff:
            type(self).objects.filter(pk=self.pk).update(is_staff=should_be_staff)
            self.is_staff = should_be_staff

        # 2) reset de M2M
        self.groups.clear()
        self.user_permissions.clear()

        if self.role == UserRole.LIBRARIAN and not self.is_superuser:
            # Grupo opcional "Bibliotecario"
            try:
                g = Group.objects.get(name="Bibliotecario")
                self.groups.add(g)
            except Group.DoesNotExist:
                pass

            # Permisos mínimos (ajusta a tu política)
            try:
                ct_libros = ContentType.objects.get(app_label="libros", model="libro")
                perms_libros = Permission.objects.filter(
                    content_type=ct_libros,
                    codename__in=["view_libro", "add_libro", "change_libro"],
                )
                self.user_permissions.add(*perms_libros)
            except ContentType.DoesNotExist:
                pass

            try:
                ct_regs = ContentType.objects.get(app_label="registros", model="registro")
                perms_regs = Permission.objects.filter(
                    content_type=ct_regs,
                    codename__in=["view_registro"],
                )
                self.user_permissions.add(*perms_regs)
            except ContentType.DoesNotExist:
                pass

    # ---------- ÚNICO save ----------
    def save(self, *args, **kwargs):
        # Si estamos creando y falta no_credencial, generar
        if self._state.adding and not self.no_credencial and self.biblioteca:
            self.generate_no_credencial()

        # Guardamos primero (necesitamos pk para M2M)
        super().save(*args, **kwargs)

        # Ya con pk, aplicamos grupos/permisos según rol
        self.apply_role_policy()
